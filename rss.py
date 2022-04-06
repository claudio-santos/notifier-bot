import time
import traceback
from datetime import datetime
from pprint import pprint

import feedparser
from discord_webhook import DiscordWebhook, DiscordEmbed

import myutils
from myutils import find


def main(_test, _console, _verbose, _conf_path, _data_path):
    global test, console, verbose, conf_path, data_path, conf, data

    test = _test
    console = _console
    verbose = _verbose
    conf_path = _conf_path
    data_path = _data_path

    conf = myutils.load_json(conf_path)
    data = myutils.load_json(data_path)

    try:
        rss_posts()
    except:
        if verbose:
            DiscordWebhook(
                url=conf['discord_url'],
                content=traceback.format_exc()
            ).execute()
        pass


def rss_posts():
    rss = feedparser.parse(conf['rss_url'])

    if not test:
        rss_normal(rss)
    else:
        rss_test(rss)


def rss_normal(rss):
    ids = {}

    for post in rss[conf['entries']]:
        post_id = str(find(conf['id'], post))
        post_value = datetime.now().timestamp()

        ids[post_id] = post_value

        if post_id not in data.keys():
            data[post_id] = post_value
        else:
            continue

        rss_post(rss, post)

    if ids:
        delta = 3 if not conf.get('delta') else conf.get('delta')
        myutils.save_data(data_path, data, ids, delta)


def rss_test(rss):
    post = rss[conf['entries']][0]
    if post:
        rss_post(rss, post)


def rss_post(rss, post):
    if not console:
        gen_webhook(post, rss).execute()
    else:
        pprint(post)


def gen_webhook(post, rss):
    webhook = DiscordWebhook(
        url=conf['discord_url'],
        username=find(conf['username'], post if conf['e']['username'] else rss),
        avatar_url=find(conf['avatar_url'], post if conf['e']['avatar_url'] else rss),
        content=myutils.clean_html(find(conf['content'], post if conf['e']['content'] else rss)),
        rate_limit_retry=True
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


if __name__ == '__main__':
    test = True
    console = False
    verbose = True
    conf_path = 'conf.json'
    data_path = 'data.json'
    main(test, console, verbose, conf_path, data_path)
