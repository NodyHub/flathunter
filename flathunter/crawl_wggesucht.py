import logging
import requests
import re
from bs4 import BeautifulSoup


class CrawlWgGesucht:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://www\.wg-gesucht\.de')

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        self.__log__.debug("Got search URL %s" % search_url)

        # load first page
        soup = self.get_page(search_url)

        # extract additional pages
        page_urls = []
        a_paginations = soup.find_all("a", class_="a-pagination")
        for a_pagination in a_paginations:
            # for each additional page
            page_urls.append("https://www.wg-gesucht.de/" + a_pagination.get('href'))

        self.__log__.info('Found pages: ' + str(len(page_urls)+1))

        # get data from first page
        entries = self.extract_data(soup)
        self.__log__.debug('Number of found entries: ' + str(len(entries)))

        # iterate over all remaining pages
        current_page_no = 2
        for page_url in page_urls:
            self.__log__.debug('Checking page %i' % current_page_no)
            soup = self.get_page(page_url)
            entries.extend(self.extract_data(soup))
            self.__log__.debug('Number of found entries: ' + str(len(entries)))
            current_page_no += 1

        return entries

    def get_page(self, search_url):
        # search_url must be specific page - cannot add page number manually
        resp = requests.get(search_url)
        if resp.status_code != 200:
            self.__log__.error("Got response (%i): %s" % (resp.status_code, resp.content))
        return BeautifulSoup(resp.content, 'lxml')

    def extract_data(self, soup):
        entries = []

        findings = soup.find_all(lambda e: e.has_attr('id') and e['id'].startswith('liste-'))
        existingFindings = list(
            filter(lambda e: e.has_attr('class') and not 'display-none' in e['class'], findings))

        baseurl = 'https://www.wg-gesucht.de/'
        for row in existingFindings:
            infostring = row.find(
                lambda e: e.name == "div" and e.has_attr('class') and 'list-details-panel-inner' in e[
                    'class']).p.text.strip()
            rooms = "1?"  # re.findall(r'\d[-]Zimmer[-]Wohnung', infostring)[0][:1]
            date = re.findall(r'\d{2}.\d{2}.\d{4}', infostring)[0]
            detail = row.find_all(lambda e: e.name == "a" and e.has_attr('class') and 'detailansicht' in e['class']);
            title = detail[2].text.strip()
            url = baseurl + detail[0]["href"]
            size_price = detail[0].text.strip()
            price = re.findall(r'\d{2,4}\s€', size_price)[0]
            size = re.findall(r'\d{2,4}\sm²', size_price)[0]

            details = {
                'id': int(url.split('.')[-2]),
                'url': url,
                'title': title,
                'price': price,
                'size': size,
                'rooms': rooms + " Zi.",
                'address': url,
                'date': date,
            }
            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))

        return entries

    def load_address(self, url):
        # extract address from expose itself
        r = requests.get(url)
        flat = BeautifulSoup(r.content, 'lxml')
        try:
            address = ' '.join(flat.find('div', {"class": "col-sm-4 mb10"}).find("a", {"href": "#"}).text.strip().split())
        except:
            address = "?"
        return address
