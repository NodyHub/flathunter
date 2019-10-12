import logging, requests, re
from bs4 import BeautifulSoup


class CrawlImmobilienscout:
    __log__ = logging.getLogger(__name__)
    URL_PATTERN = re.compile(r'https://www\.immobilienscout24\.de')

    def __init__(self):
        logging.getLogger("requests").setLevel(logging.WARNING)

    def get_results(self, search_url):
        # convert to paged URL
        if '/P-' in search_url:
            search_url = re.sub(r"/Suche/(.+?)/P-\d+", "/Suche/\1/P-[pageno]", search_url)
        else:
            search_url = re.sub(r"/Suche/(.+?)/", r"/Suche/\1/P-[pageno]/", search_url)
        self.__log__.debug("Got search URL %s" % search_url)

        # load first page to get number of entries
        page_no = 1
        soup = self.get_page(search_url, page_no)
        no_of_results = int(
            soup.find_all(lambda e: e.has_attr('data-is24-qa') and e['data-is24-qa'] == 'resultlist-resultCount')[
                0].text)
        self.__log__.info('Number of results: ' + str(no_of_results))

        # get data from first page
        entries = self.extract_data(soup)

        # iterate over all remaining pages
        num_empty_pages = 0
        num_entries = len(entries)
        while num_entries < no_of_results and num_empty_pages < 5:
            self.__log__.debug('Next Page')
            page_no += 1
            soup = self.get_page(search_url, page_no)
            new_entries = self.extract_data(soup)
            num_entries += len(new_entries)

            if new_entries == 0:
                num_empty_pages += 1

            entries.extend(new_entries)

        return entries

    def get_page(self, search_url, page_no):
        url = search_url.replace("[pageno]", str(page_no), 1)
        return self.get_generic_page(url)

    def get_generic_page(self, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            self.__log__.error("Got response (%i): %s" % (resp.status_code, resp.content))
        return BeautifulSoup(resp.content, 'html.parser')

    def extract_data(self, soup):
        entries = []

        title_elements = soup.find_all(lambda e: e.has_attr('class') and 'result-list-entry__brand-title' in e['class'])
        expose_ids = list(map(lambda e: int(e.parent['href'].split('/')[-1].replace('.html', '')), title_elements))
        expose_urls = list(map(lambda id: 'https://www.immobilienscout24.de/expose/' + str(id), expose_ids))
        attr_container_els = soup.find_all(lambda e: e.has_attr('data-is24-qa') and e['data-is24-qa'] == "attributes")
        address_fields = soup.find_all(lambda e: e.has_attr('class') and 'result-list-entry__address' in e['class'])

        for idx, title_el in enumerate(title_elements):
            attr_els = attr_container_els[idx].find_all('dd')
            address = address_fields[idx].text.strip()
            details = {
                'id': expose_ids[idx],
                'url': expose_urls[idx],
                'title': title_el.text.strip().replace('NEU', ''),
                'price': attr_els[0].text.strip().split(' ')[0].strip(),
                'size': attr_els[1].text.strip().split(' ')[0].strip() + " qm",
                'rooms': attr_els[2].text.strip().split(' ')[0].strip() + " Zi.",
                'address': address
            }
            entries.append(details)

        self.__log__.debug('extracted: ' + str(entries))
        return entries

    def load_date(self, url):
        # extract address from expose itself
        soup = self.get_generic_page(url)

        bezugsfrei_elements = soup.find_all(lambda e: e.has_attr("class") and "is24qa-bezugsfrei-ab" in e["class"])
        bezugsfrei_date = "?"
        if bezugsfrei_elements:
            bezugsfrei_date = bezugsfrei_elements[0].text.strip()

        return bezugsfrei_date

