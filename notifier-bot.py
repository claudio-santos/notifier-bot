import argparse

import facebook
import rss

description = 'Scrapes webpages and sends new items to a discord webhook.\n' \
              'Parses the webpage url in conf.json, saves post ids in data.json.'

parser = argparse.ArgumentParser(description=description)

parser.add_argument('-t', '--test', action='store_true',
                    help='runs the script for the latest entry')

parser.add_argument('-c', '--console', action='store_true',
                    help='prints output to console')

parser.add_argument('-v', '--verbose', action='store_true',
                    help='sends exceptions to discord webhook')

required = parser.add_argument_group('required arguments')

required.add_argument('-p', '--parser', type=str.lower, choices=['rss', 'facebook'], required=True,
                      help='which parser to use')

positional = parser.add_argument_group('positional arguments')

positional.add_argument('conf', type=str, nargs='?', default='conf.json',
                        help='path to the config json file (default "conf.json")')

positional.add_argument('data', type=str, nargs='?', default='data.json',
                        help='path to the data json file (default "data.json")')

if __name__ == '__main__':
    args = parser.parse_args()

    if args.parser == 'rss':
        print('parsing rss...')
        rss.main(args.test, args.console, args.verbose, args.conf, args.data)
        print('finished.')

    elif args.parser == 'facebook':
        print('parsing facebook...')
        facebook.main(args.test, args.console, args.verbose, args.conf, args.data)
        print('finished.')
