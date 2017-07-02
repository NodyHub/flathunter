import urllib.parse
import requests
import time
import logging
from datetime import datetime, timedelta

GM_MODE_TRANSIT = 'transit'
GM_MODE_BICYCLE = 'bicycling'
GM_MODE_DRIVING = 'driving'

__logger__ = logging.getLogger(__name__)


def get_distance(config, address, dest, mode):
    # get timestamp for next monday at 9:00:00 o'clock
    now = datetime.today().replace(hour=9,minute=0,second=0)
    nextMonday = now + timedelta(days=(7-now.weekday()))
    arrival_time = str(int(time.mktime(nextMonday.timetuple())))

    # decode from unicode and url encode addresses
    address = urllib.parse.quote_plus(address.strip().encode('utf8'))
    dest = urllib.parse.quote_plus(dest.strip().encode('utf8'))
    __logger__.debug("Got address: %s" % address)

    # get google maps config stuff
    base_url = config.get('google_maps_api',dict()).get('url')
    gm_key = config.get('google_maps_api',dict()).get('key')

    if not gm_key and mode != GM_MODE_DRIVING:
        __logger__.warning("No Google Maps API key configured and without using a mode different from 'driving' is not "
                           "allowed. Downgrading to mode 'drinving' thus. ")
        mode = 'driving'
        base_url = base_url.replace('&key={key}', '')

    # retrieve the result
    url = base_url.format(dest=dest, mode=mode, origin=address, key=gm_key, arrival=arrival_time)
    result = requests.get(url).json()
    if result['status'] != 'OK':
        __logger__.error("Failed retrieving distance to address %s: " % address, result)
        return None

    # get the fastest route
    distances = dict()
    for row in result['rows']:
        for element in row['elements']:
            if 'status' in element and element['status'] != 'OK':
                __logger__.warning("For address %s we got the status message: %s" % (address,element['status']))
                __logger__.debug("We got this result: %s" % repr(result))
                continue
            __logger__.debug("Got distance and duration: %s / %s (%i seconds)" % (element['distance']['text'], element['duration']['text'], element['duration']['value']))
            distances[element['duration']['value']] = '%s (%s)' % (element['duration']['text'], element['distance']['text'])

    return distances[min(distances.keys())] if distances else None

