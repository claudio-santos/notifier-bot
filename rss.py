import sys
import time

import feedparser
from discord_webhook import DiscordWebhook, DiscordEmbed

import myutils
from myutils import find

arg1 = sys.argv[1] if len(sys.argv) > 1 else 'conf.json'
arg2 = sys.argv[2] if len(sys.argv) > 2 else 'data.json'

conf = myutils.load_json(arg1)
data = myutils.load_json(arg2)

rss_url = conf['rss_url']
rss_webhook = conf['discord_url']


#   Needs data.json like:
#   {
#       "post_ids": []
#   }

#   Needs conf.json like:
#   {
#       "rss_url":"",
#       "discord_url":"",
#       "entries":"entries",
#       "username":"",
#       "avatar_url":"",
#       "content":"",
#       "author":{
#           "name":"",
#           "url":"",
#           "icon_url":""
#       },
#       "title":"",
#       "url":"",
#       "description":"",
#       "thumbnail":{
#           "url":""
#       },
#       "image":{
#           "url":""
#       },
#       "footer":{
#           "text":"",
#           "icon_url":""
#       },
#       "e":{
#           "username":false,
#           "avatar_url":false,
#           "content":false,
#           "author":{
#               "name":false,
#               "url":false,
#               "icon_url":false
#           },
#           "title":false,
#           "url":false,
#           "description":false,
#           "thumbnail":{
#               "url":false
#           },
#           "image":{
#               "url":false
#           },
#           "footer":{
#               "text":false,
#               "icon_url":false
#           }
#       }
#   }


def rss_posts():
    rss = feedparser.parse(rss_url)
    ids = []

    for post in rss[conf['entries']]:
        post_id = find(conf['id'], post)

        if post_id in data['post_ids']:
            ids.append(post_id)
            continue
        ids.append(post_id)

        gen_webhook(post, rss).execute()

    data['post_ids'] = ids
    myutils.dump_json('data.json', data)


def gen_webhook(post, rss):
    webhook = DiscordWebhook(
        url=rss_webhook,
        username=find(conf['username'], post if conf['e']['username'] else rss),
        avatar_url=find(conf['avatar_url'], post if conf['e']['avatar_url'] else rss),
        content=myutils.clean_html(find(conf['content'], post if conf['e']['content'] else rss)),
    )

    imgs = myutils.get_imgs(find(conf['image']['url'], post if conf['e']['image']['url'] else rss))

    for img in imgs:
        embed = DiscordEmbed()
        embed.set_image(url=img['src'])
        embed.set_footer(text=img['alt'])
        webhook.add_embed(embed)

    embed = DiscordEmbed(
        title=find(conf['title'], post if conf['e']['title'] else rss),
        url=find(conf['url'], post if conf['e']['url'] else rss),
        description=myutils.clean_html(find(conf['description'], post if conf['e']['description'] else rss)),
    )
    embed.set_author(
        name=find(conf['author']['name'], post if conf['e']['author']['name'] else rss),
        icon_url=find(conf['author']['icon_url'], post if conf['e']['author']['icon_url'] else rss),
        url=find(conf['author']['url'], post if conf['e']['author']['url'] else rss)
    )
    embed.set_thumbnail(
        url=find(conf['thumbnail']['url'], post if conf['e']['thumbnail']['url'] else rss)
    )
    embed.set_footer(
        text=time.strftime(
            '%A, %d %B %Y, %H:%M',
            find(conf['footer']['text'], post if conf['e']['footer']['text'] else rss)
        ),
        icon_url=find(conf['footer']['icon_url'], post if conf['e']['footer']['icon_url'] else rss)
    )
    webhook.add_embed(embed)

    return webhook


def test():
    rss = feedparser.parse(rss_url)
    print(rss)


if __name__ == '__main__':
    rss_posts()
    # test()
