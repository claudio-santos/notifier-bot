# notifier-bot

```text
usage: notifier-bot.py [-h] [-t] [-c] -p {rss,facebook} [conf] [data]

Scrapes webpages and sends new items to a discord webhook. Parses the webpage
url in conf.json, saves post ids in data.json.

optional arguments:
  -h, --help            show this help message and exit
  -t, --test            runs the script for the latest entry
  -c, --console         prints output to console

required arguments:
  -p {rss,facebook}, --parser {rss,facebook}
                        which parser to use

positional arguments:
  conf                  path to the config json file (default "conf.json")
  data                  path to the data json file (default "data.json")
```

#### facebook-scraper
Parses the facebook_url in conf.json. \
Saves post ids and timestamps in data.json.

Needed conf.json:
```json
{
   "facebook_url":"",
   "discord_url":"",
   "id":"post_id",
   "username":"username",
   "avatar_url":"image_lowquality",
   "content":"text",
   "author":{
      "name":"link",
      "url":"link",
      "icon_url":""
   },
   "title":"",
   "url":"",
   "description":"",
   "thumbnail":{
      "url":""
   },
   "image":{
      "url":"images"
   },
   "footer":{
      "text":"timestamp",
      "icon_url":""
   }
}
```

#### feedparser
Parses the rss_url in conf.json. \
Saves post ids and timestamps in data.json. \
Fields "e" true if entry or false if feed.

Needed conf.json:
```json
{
   "rss_url":"",
   "discord_url":"",
   "entries":"entries",
   "id":"id",
   "username":"feed.title",
   "avatar_url":"feed.image.href",
   "content":"title",
   "author":{
      "name":"author",
      "url":"link",
      "icon_url":""
   },
   "title":"",
   "url":"",
   "description":"",
   "thumbnail":{
      "url":""
   },
   "image":{
      "url":"summary"
   },
   "footer":{
      "text":"published_parsed",
      "icon_url":""
   },
   "e":{
      "username":false,
      "avatar_url":false,
      "content":true,
      "author":{
         "name":true,
         "url":true,
         "icon_url":false
      },
      "title":false,
      "url":false,
      "description":false,
      "thumbnail":{
         "url":false
      },
      "image":{
         "url":true
      },
      "footer":{
         "text":true,
         "icon_url":false
      }
   }
}
```

Examples:

![](readme/ex1.jpg)

![](readme/ex2.jpg)

![](readme/ex3.jpg)
