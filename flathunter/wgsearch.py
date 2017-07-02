import logging
import requests
import re
from bs4 import BeautifulSoup

class WGSearcher:
    URL_PATTERN = re.compile(r'https://www\.wg-gesucht\.de')
    __log__ = logging.getLogger(__name__)

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        self.__log__.debug("Got search URL %s" % search_url)

        # load first page
        page_no = 0
        soup = self.get_page(search_url, page_no)
        no_of_pages = 0  # TODO get it from soup
        self.__log__.info('Found pages: ' + str(no_of_pages))

        # get data from first page
        entries = self.extract_data(soup)
        self.__log__.debug('Number of found entries: ' + str(len(entries)))

        # iterate over all remaining pages
        while (page_no + 1) < no_of_pages:  # page_no starts with 0, no_of_pages with 1
            page_no += 1
            self.__log__.debug('Checking page %i' % page_no)
            soup = self.get_page(search_url, page_no)
            entries.extend(self.extract_data(soup))
            self.__log__.debug('Number of found entries: ' + str(len(entries)))

        return entries

    def get_page(self, search_url, page_no):
        resp = requests.get(search_url)  # TODO add page_no in url
        if resp.status_code != 200:
            self.__log__.error("Got response (%i): %s" % (resp.status_code, resp.content))
        return BeautifulSoup(resp.content, 'html.parser')

    def extract_data(self, soup):
        entries = []

        findings = soup.find_all(lambda e: e.has_attr('id') and e['id'].startswith('ad--'))
        existingFindings = list(
            filter(lambda e: e.has_attr('class') and not 'listenansicht-inactive' in e['class'], findings))

        baseurl = 'https://www.wg-gesucht.de/'
        for row in existingFindings:
            url = baseurl + row['adid']  # u'wohnungen-in-Muenchen-Altstadt-Lehel.6038357.html'
            id = int(url.split('.')[-2])
            rooms = row.find(lambda e: e.has_attr('class') and 'ang_spalte_zimmer' in e['class']).text.strip()  # u'3'
            price = row.find(
                lambda e: e.has_attr('class') and 'ang_spalte_miete' in e['class']).text.strip()  # u'433\u20ac'
            size = row.find(
                lambda e: e.has_attr('class') and 'ang_spalte_groesse' in e['class']).text.strip()  # u'75m\xb2'
            district = row.find(
                lambda e: e.has_attr('class') and 'ang_spalte_stadt' in e['class']).text.strip()  # u'Altstadt-Lehel'
            date = row.find(
                lambda e: e.has_attr('class') and 'ang_spalte_freiab' in e['class']).text.strip()  # u'21.03.17'

            details = {
                'id': int(url.split('.')[-2]),
                'url': url,
                'title': "Wohnung in %s ab dem %s" % (district, date),
                'price': price,
                'size': size,
                'rooms': rooms + " Zi.",
                'address': url
            }
            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))

        return entries

    def load_address(self, url):
        # extract address from expose itself
        exposeHTML = requests.get(url).content
        exposeSoup = BeautifulSoup(exposeHTML, 'html.parser')
        address_raw = exposeSoup.find(lambda e: e.has_attr('onclick') and '#map_tab' in e['onclick']).text
        address = address_raw.strip().split('\n')[0] + ", " + address_raw.strip().split('\n')[-1].strip()

        return address
