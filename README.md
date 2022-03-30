# notifier-bot

Parses webpages and notifies to a discord webhook.

First version uses facebook-scraper on a single facebook page.

Call facebook.py to run, put it in a cron job.

Needs .env \
FACEBOOK_ACCOUNT=(name of the page) \
FACEBOOK_POSTED=(initially empty, used to save parsed posts) \
FACEBOOK_WEBHOOK=(discord webhook for this parser) \

Hardcoded parsed fields and generated webhook.
