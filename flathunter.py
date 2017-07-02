#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Jan Harrie"
__version__ = "1.0"
__maintainer__ = "Jan Harrie"
__email__ = "harrymcfly@protonmail.com"
__status__ = "Production"

import argparse, os, logging, time, yaml, re, urllib.parse, requests

from flathunter.immosearch import ImmoSearcher
from flathunter.wgsearch import WGSearcher
from flathunter.idmaintainer import IdMaintainer
import flathunter.util as util


def hunt_flats(config, searchers, id_watch):
    logger = logging.getLogger()
    bot_token = config.get('telegram', dict()).get('bot_token', '')
    receiver_ids = config.get('telegram', dict()).get('receiver_ids', list())
    new_links = 0
    processed = id_watch.get()

    for url in config.get('urls', list()):
        logger.debug('Processing URL: ' + url)

        try:
            for searcher in searchers:
                if re.search(searcher.URL_PATTERN, url):
                    results = searcher.get_results(url)
                    break
        except requests.exceptions.ConnectionError:
            logger.warning("Connection to %s failed. Retrying. " % url.split('/')[2])
            continue

        # on error, stop execution
        if not results:
            break

        for expose in results:
            # check if already processed
            if expose['id'] in processed:
                continue

            logger.info('New offer: ' + expose['title'])

            # to reduce traffic, some addresses need to be loaded on demand
            address = expose['address']
            if address.startswith('http'):
                url = address
                for searcher in searchers:
                    if re.search(searcher.URL_PATTERN, url):
                        address = searcher.load_address(url)
                        logger.debug("Loaded address %s for url %s" % (address, url))
                        break

            # calculdate durations
            message = config.get('message', "").format(
                title=expose['title'],
                rooms=expose['rooms'],
                size=expose['size'],
                price=expose['price'],
                url=expose['url'],
                durations=get_formatted_durations(config, address)).strip()

            # send message to all receivers
            for receiver_id in receiver_ids:
                send_msg(bot_token, receiver_id, message)

            new_links = new_links + 1
            id_watch.add(expose['id'])

    logger.info(str(new_links) + ' new offer found')


def send_msg(bot_token, chat_id, message):
    logger = logging.getLogger()

    url = 'https://api.telegram.org/%s/sendMessage?chat_id=%i&text=%s'
    text = urllib.parse.quote_plus(message.encode('utf-8'))
    qry = url % (bot_token, chat_id, text)
    logger.debug("Retrieving URL %s" % qry)
    resp = requests.get(qry)
    logger.debug("Got response (%i): %s" % (resp.status_code, resp.content))
    data = resp.json()

    # handle error
    if resp.status_code != 200:
        sc = resp.status_code
        logger.error("When sending bot message, we got status %i with message: %s" % (sc, data))


def get_formatted_durations(config, address):
    out = ""
    for duration in config.get('durations', list()):
        if 'destination' in duration and 'name' in duration:
            dest = duration.get('destination')
            name = duration.get('name')
            for mode in duration.get('modes', list()):
                if 'gm_id' in mode and 'title' in mode:
                    duration = util.getDistance(config, address, dest, mode['gm_id'])
                    out += "> %s (%s): %s\n" % (name, mode['title'], duration)

    return out.strip()


def launch_flat_hunt(config):
    searchers = [ImmoSearcher(), WGSearcher()]
    id_watch = IdMaintainer('./processed_ids.db')

    hunt_flats(config, searchers, id_watch)
    while config.get('loop', dict()).get('active', False):
        hunt_flats(config, searchers, id_watch)
        time.sleep(config.get('loop', dict()).get('sleepting_time', 10))


def main():
    # init logging
    cyellow = '\033[93m'
    cblue = '\033[94m'
    coff = '\033[0m'
    logging.basicConfig(
        format='[' + cblue + '%(asctime)s' + coff + '|' + cblue + '%(filename)-18s' + coff + '|' \
               + cyellow + '%(levelname)-8s' + coff + ']: %(message)s',
        datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)
    logger = logging.getLogger()

    # parse args
    parser = argparse.ArgumentParser(description="Searches for flats on Immobilienscout24.de and " \
                                                 "wg-gesucht.de and sends results to Telegram User",
                                     epilog="Designed by Nody")
    parser.add_argument('--config', '-c', type=argparse.FileType('r', encoding='UTF-8'),
                        default='%s/config.yaml' % os.path.dirname(os.path.abspath(__file__)),
                        help="Config file to use. If not set, try to use '%s/config.yaml' " % os.path.dirname(os.path.abspath(__file__)))
    args = parser.parse_args()

    # load config
    configHandle = args.config
    logger.info("Using config %s" % configHandle.name)
    config = yaml.load(configHandle.read())

    # check config
    if not config.get('telegram', dict()).get('bot_token'):
        logger.error("No telegram bot token configured. Starting like this would be meaningless...")
        return
    if not config.get('telegram', dict()).get('receiver_ids'):
        logger.error("No telegram receivers configured. Starting like this would be meaningless...")
        return
    if not config.get('urls'):
        logger.error("No urls configured. Starting like this would be meaningless...")
        return

    # adjust log level, if required
    if config.get('verbose'):
        logger.setLevel(logging.DEBUG)
        from pprint import pformat
        logger.debug("Settings from config: %s" % pformat(config))

    # start hunting for flats
    launch_flat_hunt(config)


if __name__ == "__main__":
    main()
