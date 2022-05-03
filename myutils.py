import json
from datetime import datetime

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta


def load_json(filename):
    res = {}
    try:
        with open(filename) as file:
            res = json.load(file)
    except:
        pass
    return res


def dump_json(filename, data):
    with open(filename, 'w+') as file:
        json.dump(data, file)


def save_data(filename, data, ids, months):
    for key, value in dict(data).items():
        date_saved = datetime.fromtimestamp(value)
        date_check = datetime.now() - relativedelta(months=months)
        if date_saved < date_check and key not in ids.keys():
            del data[key]

    dump_json(filename, data)


def find(element, json_data):
    if not element:
        return ''
    keys = element.split('.')
    data = json_data
    for key in keys:
        if key not in data:
            return ''
        data = data[key] if type(data[key]) is not list else data[key][0]
    return data


def get_imgs(post_imgs):
    imgs = []

    if not post_imgs:
        return imgs

    if type(post_imgs) is list:
        for x in post_imgs:
            imgs.append({'src': x, 'alt': ''})
        return imgs

    if bool(BeautifulSoup(post_imgs, 'html.parser').find()) is False:
        if post_imgs.lower().startswith('http'):
            imgs.append({'src': post_imgs, 'alt': ''})
        return imgs

    xs = BeautifulSoup(post_imgs, 'html.parser').find_all('img')
    for x in xs:
        src = ''
        alt = ''
        try:
            src = x['src']
        except:
            pass
        try:
            alt = x['alt']
        except:
            pass
        imgs.append({'src': src, 'alt': alt})
    return imgs


def text_html(string):
    if bool(BeautifulSoup(string, 'html.parser').find()) is False:
        return string
    string = BeautifulSoup(string, 'html.parser').text
    return string


def clean_html(string):
    string = string.replace('<br />', '\n')
    if bool(BeautifulSoup(string, 'html.parser').find()) is False:
        return string
    soup = BeautifulSoup(string, 'html.parser')
    string = soup.prettify().strip()
    for x in soup.find_all():
        string = string.replace(x.prettify().strip(), '').strip()
    return string


if __name__ == "__main__":
    print('myutils.py')
