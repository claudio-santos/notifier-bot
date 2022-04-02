import datetime
import sys

from discord_webhook import DiscordWebhook, DiscordEmbed
from facebook_scraper import get_posts

import myutils
from myutils import find

arg1 = sys.argv[1] if len(sys.argv) > 1 else 'conf.json'
arg2 = sys.argv[2] if len(sys.argv) > 2 else 'data.json'

conf = myutils.load_json(arg1)
data = myutils.load_json(arg2)

facebook_account = conf['facebook_url']
facebook_webhook = conf['discord_url']


#   Needs data.json like:
#   {
#       "post_ids": []
#   }

#   Needs conf.json like:
#   {
#       "facebook_url":"",
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


def facebook_posts():
    ids = []

    for post in get_posts(account=facebook_account, pages=2):
        post_id = find(conf['id'], post)

        if post_id in data['post_ids']:
            ids.append(post_id)
            continue
        ids.append(post_id)

        gen_webhook(post).execute()

    data['post_ids'] = ids
    myutils.dump_json(arg2, data)


def gen_webhook(post):
    webhook = DiscordWebhook(
        url=facebook_webhook,
        username=find(conf['username'], post),
        avatar_url=find(conf['avatar_url'], post),
        content=myutils.clean_html(find(conf['content'], post)),
    )

    imgs = myutils.get_imgs(find(conf['image']['url'], post))

    for img in imgs:
        embed = DiscordEmbed()
        embed.set_image(url=img['src'])
        embed.set_footer(text=img['alt'])
        webhook.add_embed(embed)

    embed = DiscordEmbed(
        title=find(conf['title'], post),
        url=find(conf['url'], post),
        description=myutils.clean_html(find(conf['description'], post)),
    )
    embed.set_author(
        name=find(conf['author']['name'], post),
        icon_url=find(conf['author']['icon_url'], post),
        url=find(conf['author']['url'], post)
    )
    embed.set_thumbnail(
        url=find(conf['thumbnail']['url'], post)
    )
    embed.set_footer(
        text=datetime.datetime.fromtimestamp(
            find(conf['footer']['text'], post)
        ).strftime('%A, %d %B %Y, %H:%M'),
        icon_url=find(conf['footer']['icon_url'], post)
    )
    webhook.add_embed(embed)

    return webhook


def test():
    rss = get_posts(account=facebook_account, pages=2)
    for post in rss:
        print(post)


if __name__ == "__main__":
    facebook_posts()
    # test()
