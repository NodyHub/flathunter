#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import logging
import time
import yaml
from flathunter.crawl_immobilienscout import CrawlImmobilienscout
from flathunter.crawl_wggesucht import CrawlWgGesucht
from flathunter.idmaintainer import IdMaintainer
from flathunter.hunter import Hunter
from flathunter.crawl_ebaykleinanzeigen import CrawlEbayKleinanzeigen

__author__ = "Jan Harrie"
__version__ = "1.0"
__maintainer__ = "Nody"
__email__ = "harrymcfly@protonmail.com"
__status__ = "Production"

# init logging
if os.name == 'posix':
    # coloring on linux
    cyellow = '\033[93m'
    cblue = '\033[94m'
    coff = '\033[0m'
    format = '[' + cblue + '%(asctime)s' + coff + '|' + cblue + '%(filename)-18s' + coff + '|' + cyellow + \
             '%(levelname)-8s' + coff + ']: %(message)s'
else:
    # else without color
    format = '[%(asctime)s|%(filename)-18s|%(levelname)-8s]: %(message)s',
logging.basicConfig(
    format=format,
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.DEBUG)
__log__ = logging.getLogger(__name__)


def launch_flat_hunt(config):
    searchers = [CrawlImmobilienscout(), CrawlWgGesucht(),CrawlEbayKleinanzeigen()]
    id_watch = IdMaintainer('%s/processed_ids.db' % os.path.dirname(os.path.abspath(__file__)))

    hunter = Hunter()
    hunter.hunt_flats(config, searchers, id_watch)

    while config.get('loop', dict()).get('active', False):
        time.sleep(config.get('loop', dict()).get('sleeping_time',60*10))
        hunter.hunt_flats(config, searchers, id_watch)


def main():
    # parse args
    parser = argparse.ArgumentParser(description="Searches for flats on Immobilienscout24.de and wg-gesucht.de and "
                                                 "sends results to Telegram User", epilog="Designed by Nody")
    parser.add_argument('--config', '-c',
                        type=argparse.FileType('r'),
                        default='%s/config.yaml' % os.path.dirname(os.path.abspath(__file__)),
                        help="Config file to use. If not set, try to use '%s/config.yaml' " %
                             os.path.dirname(os.path.abspath(__file__))
                        )
    args = parser.parse_args()

    # load config
    config_handle = args.config
    __log__.info("Using config %s" % config_handle.name)
    config = yaml.load(config_handle.read())

    # check config
    if not config.get('telegram', dict()).get('bot_token'):
        __log__.error("No telegram bot token configured. Starting like this would be meaningless...")
        return
    if not config.get('telegram', dict()).get('receiver_ids'):
        __log__.error("No telegram receivers configured. Starting like this would be meaningless...")
        return
    if not config.get('urls'):
        __log__.error("No urls configured. Starting like this would be meaningless...")
        return

    # adjust log level, if required
    if config.get('verbose'):
        __log__.setLevel(logging.DEBUG)
        from pprint import pformat
        __log__.debug("Settings from config: %s" % pformat(config))

    # start hunting for flats
    launch_flat_hunt(config)


if __name__ == "__main__":
    main()
