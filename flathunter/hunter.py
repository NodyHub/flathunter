import logging
import requests
import re
import urllib
import datetime
import time
from flathunter.sender_telegram import SenderTelegram

class Hunter:
    __log__ = logging.getLogger(__name__)
    GM_MODE_TRANSIT = 'transit'
    GM_MODE_BICYCLE = 'bicycling'
    GM_MODE_DRIVING = 'driving'

    def hunt_flats(self, config, searchers, id_watch):
        sender = SenderTelegram(config)
        new_links = 0
        processed = id_watch.get()

        for url in config.get('urls', list()):
            self.__log__.debug('Processing URL: ' + url)

            try:
                for searcher in searchers:
                    if re.search(searcher.URL_PATTERN, url):
                        results = searcher.get_results(url)
                        break
            except requests.exceptions.ConnectionError:
                self.__log__.warning("Connection to %s failed. Retrying. " % url.split('/')[2])
                continue

            # on error, stop execution
            if not results:
                break

            for expose in results:
                # check if already processed
                if expose['id'] in processed:
                    continue

                self.__log__.info('New offer: ' + expose['title'])

                # to reduce traffic, some addresses need to be loaded on demand
                address = expose['address']
                if address.startswith('http'):
                    url = address
                    for searcher in searchers:
                        if re.search(searcher.URL_PATTERN, url):
                            address = searcher.load_address(url)
                            self.__log__.debug("Loaded address %s for url %s" % (address, url))
                            break

                # calculdate durations
                message = config.get('message', "").format(
                    title=expose['title'],
                    rooms=expose['rooms'],
                    size=expose['size'],
                    price=expose['price'],
                    url=expose['url']
                    ).strip()

                # send message to all receivers
                sender.send_msg(message)

                new_links = new_links + 1
                id_watch.add(expose['id'])

        self.__log__.info(str(new_links) + ' new offer found')
