import datetime
import os

from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv, set_key
from facebook_scraper import get_posts

load_dotenv()

facebook_account = os.getenv('FACEBOOK_ACCOUNT')
facebook_posted = os.getenv('FACEBOOK_POSTED')
facebook_webhook = os.getenv('FACEBOOK_WEBHOOK')


def facebook_posts():
    posted = ''
    for post in get_posts(account=facebook_account, pages=2):
        post_id = post['post_id']

        if post_id in facebook_posted:
            posted += post_id + ';'
            continue
        posted += post_id + ';'

        webhook = DiscordWebhook(url=facebook_webhook, content='***' + post['text'] + '***')
        embed = DiscordEmbed()
        embed.set_author(name=post['username'], url=post['link'])
        embed.set_image(url=post['image'])
        embed.set_footer(text=datetime.datetime.fromtimestamp(post['timestamp']).strftime('%A, %d %B %Y, %H:%M'))
        webhook.add_embed(embed)
        webhook.execute()

    set_key('.env', 'FACEBOOK_POSTED', posted)


def webhook_test():
    webhook = DiscordWebhook(url=facebook_webhook, content='***content***')
    embed = DiscordEmbed()
    embed.set_author(name='author_name', url='https://time.is/')
    embed.set_footer(text=datetime.datetime.now().strftime('%A, %d %B %Y, %H:%M'))
    webhook.add_embed(embed)
    webhook.execute()


if __name__ == "__main__":
    facebook_posts()
    # webhook_test()
