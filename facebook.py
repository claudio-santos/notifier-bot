import traceback
from datetime import datetime
from pprint import pprint

from discord_webhook import DiscordWebhook, DiscordEmbed
from facebook_scraper import get_posts

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
        facebook_posts()
    except:
        if verbose:
            DiscordWebhook(
                url=conf['discord_url'],
                content=traceback.format_exc()
            ).execute()
        pass


def facebook_posts():
    posts = get_posts(account=conf['facebook_url'], pages=2)

    if not test:
        facebook_normal(posts)
    else:
        facebook_test(posts)


def facebook_normal(posts):
    ids = {}

    for post in posts:
        post_id = str(find(conf['id'], post))
        post_value = datetime.now().timestamp()

        ids[post_id] = post_value

        if post_id not in data.keys():
            data[post_id] = post_value
        else:
            continue

        facebook_post(post)

    if ids:
        delta = 3 if not conf.get('delta') else conf.get('delta')
        myutils.save_data(data_path, data, ids, delta)


def facebook_test(posts):
    post = next(posts)
    if post:
        facebook_post(post)


def facebook_post(post):
    if not console:
        gen_webhook(post).execute()
    else:
        pprint(post)


def gen_webhook(post):
    webhook = DiscordWebhook(
        url=conf['discord_url'],
        username=find(conf['username'], post),
        avatar_url=find(conf['avatar_url'], post),
        content=myutils.clean_html(find(conf['content'], post)),
        rate_limit_retry=True
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
        text=datetime.fromtimestamp(
            find(conf['footer']['text'], post)
        ).strftime('%A, %d %B %Y, %H:%M'),
        icon_url=find(conf['footer']['icon_url'], post)
    )
    webhook.add_embed(embed)

    return webhook


if __name__ == "__main__":
    test = True
    console = False
    verbose = True
    conf_path = 'conf.json'
    data_path = 'data.json'
    main(test, console, verbose, conf_path, data_path)
