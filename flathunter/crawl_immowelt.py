# coding= UTF-8
import logging, requests, re
from bs4 import BeautifulSoup


class CrawlImmoWelt:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://www\.immowelt\.de')

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        self.__log__.debug("Got search URL %s" % search_url)

        soup = self.get_page(search_url)

        # get data from first page
        entries = self.extract_data(soup)
        self.__log__.debug('Number of found entries: ' + str(len(entries)))

        return entries

    def get_page(self, search_url):
        resp = requests.get(search_url)  # TODO add page_no in url
        if resp.status_code != 200:
            self.__log__.error("Got response (%i): %s" % (resp.status_code, resp.content))
        return BeautifulSoup(resp.content, 'html.parser')

    def extract_data(self, soup):
        entries = []
        soup = soup.find('div',class_ = "iw_list_content")
        #print soup
        results = soup.find_all(lambda e: e.has_attr('data-estateid') and not e.has_attr('data-action'))
        #print results
        for index,listing in enumerate(results):
            price = listing.find('div',class_="hardfact price_rent").find("strong").text.strip()
            id = listing.find('a').get('href').split('expose/',1)[1].split('?',1)[0].strip()
            id = int(id,base=36)
            url = "https://www.immowelt.de" + listing.find('a').get('href')
            size = listing.find('div',class_="hardfact ").text
            size = size.split('ca.)',1)[1].strip()
            rooms = listing.find('div',class_="hardfact rooms").text
            rooms = rooms.split('Zimmer',1)[1].strip()
            address = listing.find('div',class_="listlocation ellipsis relative").text.strip()
            title = listing.find('h2').text.strip()
            details = {
                'id': id,
                'url':  url ,
                'title': title,
                'price': price,
                'size': size,
                'rooms': rooms ,
                'address': address
            }
            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))

        return entries
