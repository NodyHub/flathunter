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
    GM_NO_KEY = 'YOUR_API_KEY'

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
                    url=expose['url'],
                    durations=self.get_formatted_durations(config, address)).strip()

                # send message to all receivers
                sender.send_msg(message)

                new_links = new_links + 1
                id_watch.add(expose['id'])

        self.__log__.info(str(new_links) + ' new offer found')

    def get_formatted_durations(self, config, address):
        out = ""
        for duration in config.get('durations', list()):
            if 'destination' in duration and 'name' in duration:
                dest = duration.get('destination')
                name = duration.get('name')
                for mode in duration.get('modes', list()):
                    if 'gm_id' in mode and 'title' in mode and 'key' in config.get('google_maps_api',dict()):
                        duration = self.get_gmaps_distance(config, address, dest, mode['gm_id'])
                        out += "> %s (%s): %s\n" % (name, mode['title'], duration)

        return out.strip()

    def get_gmaps_distance(self, config, address, dest, mode):
        # get timestamp for next monday at 9:00:00 o'clock
        now = datetime.datetime.today().replace(hour=9,minute=0,second=0)
        next_monday = now + datetime.timedelta(days=(7-now.weekday()))
        arrival_time = str(int(time.mktime(next_monday.timetuple())))

        # decode from unicode and url encode addresses
        address = urllib.parse.quote_plus(address.strip().encode('utf8'))
        dest = urllib.parse.quote_plus(dest.strip().encode('utf8'))
        self.__log__.debug("Got address: %s" % address)

        # get google maps config stuff
        base_url = config.get('google_maps_api',dict()).get('url')
        gm_key = config.get('google_maps_api',dict()).get('key')

        if (not gm_key or self.GM_NO_KEY )  and mode != self.GM_MODE_DRIVING:
            self.__log__.warning("No Google Maps API key configured and without using a mode different from "
                                    "'driving' is not allowed. Downgrading to mode 'drinving' thus. ")
            mode = 'driving'
            base_url = base_url.replace('&key={key}', '')

        # retrieve the result
        url = base_url.format(dest=dest, mode=mode, origin=address, key=gm_key, arrival=arrival_time)
        result = requests.get(url).json()
        if result['status'] != 'OK':
            self.__log__.error("Failed retrieving distance to address %s: " % str(address), str(result))
            return None

        # get the fastest route
        distances = dict()
        for row in result['rows']:
            for element in row['elements']:
                if 'status' in element and element['status'] != 'OK':
                    self.__log__.warning("For address %s we got the status message: %s" % (address,element['status']))
                    self.__log__.debug("We got this result: %s" % repr(result))
                    continue
                self.__log__.debug("Got distance and duration: %s / %s (%i seconds)"
                                   % (element['distance']['text'], element['duration']['text'],
                                      element['duration']['value'])
                                   )
                distances[element['duration']['value']] = '%s (%s)' % \
                                                          (element['duration']['text'], element['distance']['text'])
        return distances[min(distances.keys())] if distances else None

