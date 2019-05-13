import logging
import requests
import re
from bs4 import BeautifulSoup


class CrawlEbayKleinanzeigen:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://www\.ebay-kleinanzeigen\.de')

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
        soup = soup.find(id="srchrslt-adtable")
        title_elements = soup.find_all( lambda e: e.has_attr('class') and 'ellipsis' in e['class'])
        expose_ids=soup.find_all("article", class_="aditem")


        #soup.find_all(lambda e: e.has_attr('data-adid'))
        #print(expose_ids)
        for idx,title_el in enumerate(title_elements):
            print(title_el.text)
            print(title_el.get("href"))
            print(expose_ids[idx].get("data-adid"))
            price = expose_ids[idx].find("strong").text
            tags = expose_ids[idx].find_all(class_="simpletag tag-small")
            address = "https://www.ebay-kleinanzeigen.de/" +title_el.get("href")
            try:
                print(tags[0].text)
                rooms = tags[0].text
            except IndexError:
                print("Keine Zimmeranzahl gegeben")
                rooms = "Nicht gegeben"
            try:
                print(tags[1].text)
                size = tags[1].text
            except IndexError:
                size = "Nicht gegeben"
                print("Quadratmeter nicht angegeben")
            details = {
                'id': expose_ids[idx].get("data-adid"),
                'url':  address ,
                'title': title_el.text.strip(),
                'price': price,
                'size': size,
                'rooms': rooms ,
                'address': address
            }
            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))

        return entries

    def load_address(self, url):
        # extract address from expose itself
        exposeHTML = requests.get(url).content
        exposeSoup = BeautifulSoup(exposeHTML, 'html.parser')
        try:
            street_raw = exposeSoup.find(id="street-address").text
        except AttributeError:
            street_raw=""
        try:
            address_raw = exposeSoup.find(id="viewad-locality").text
        except AttributeError:
            address_raw =""
        address = address_raw.strip().replace("\n","") + " "+street_raw.strip()

        return address
