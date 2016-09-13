__author__ = "Jan Harrie"
__version__ = "0.1"
__maintainer__ = "Jan Harrie"
__email__ = "harrymcfly@protonmail.com"
__status__ = "Development"

from webscraping import common, xpath
from time import sleep
from unicodedata import normalize

#~ Logging KungFoo
import logging
log = logging.getLogger()


class WGGesuchtCrawler:

	def __init__(self, BROWSER_INSTANCE):
		# disable verbose logging from webscraping and define own level
		common.logger.setLevel(logging.CRITICAL)

		# prepare browser
		self.BROWSER=BROWSER_INSTANCE
		self.BROWSER

	def get_results(self):
		log.info('Start for search at WG-Gesucht')

		log.debug('Open Page')
		BASE_URL = 'https://www.wg-gesucht.de/wohnungen-in-Muenchen.90.2.0.0.html'
		self.BROWSER.get(BASE_URL)
		self.BROWSER.wait(3)

		log.debug('Expand Options')
		self.BROWSER.click('span[id=morefilter]')
		self.BROWSER.wait(2)

		log.debug('Make Selections')
		self.BROWSER.js('document.getElementById("zimmer_max").selectedIndex = 1;')
		self.BROWSER.js('changeSth();')
		self.BROWSER.js('document.getElementById("mietart").selectedIndex = 2;')
		self.BROWSER.js('changeSth();')
		self.BROWSER.js('document.getElementById("zeitraum").selectedIndex = 3;')
		self.BROWSER.js('changeSth();')
		self.BROWSER.fill('input[id=max_miete]', '800')
		self.BROWSER.js('changeSth();')

		log.debug('Go search for it')
		self.BROWSER.click('button[id=apply_filter]')
		self.BROWSER.wait(3)

		log.debug('Analyze Result')
		html = self.BROWSER.current_html()
		no_of_results = int(xpath.search(html, '//h1')[0].split(':')[1].strip().split(' ')[0])
		log.debug('No of Results: ' + str(no_of_results))

		raw_results = xpath.search(html, '//tr[@id="ad--.*?"]')
		results = []
		log.debug('len(raw_result):' + str(len(raw_results)))


		log.debug('Iterate over results')
		for row in raw_results:
			details = self.extract_data(row)
			log.debug('Append: ' + str(details))
			results.append(details)

		log.info('Done!')

		return results


	def get_page_html(self, url):
		self.BROWSER.get(url)
		self.BROWSER.wait(5)
		return self.BROWSER.current_html()

	def post_page_html(self, url, payload):
		self.BROWSER.post(url, payload)
		self.BROWSER.wait(5)
		return self.BROWSER.current_html()


	def extract_data(self, raw_row):

		i = 0
		details = {}

		# Get Link
		details['url'] = 'https://www.wg-gesucht.de/' + normalize('NFKD', xpath.search(raw_row, '//td/a/@href')[1]).encode('ascii','ignore')

		for row_data in xpath.search(raw_row, '//td/a/span'):

			# clean from unicode
			raw_datum = normalize('NFKD', row_data.strip()).encode('ascii','ignore')

			if i == 0:
				details['id'] = int(details['url'].split('.')[-2])
			elif i == 1:
				details['rooms'] = raw_datum
			elif i == 2:
				details['online_since'] = raw_datum
			elif i == 3:
				details['price'] = raw_datum.split('</b>')[0].replace('<b>','').strip()
			elif i == 4:
				details['size'] = raw_datum
			elif i == 5:
				details['where'] = raw_datum
			elif i == 6:
				details['starts_at'] = raw_datum

			i = i + 1
		details['title'] = details['rooms'] + ' Zimmer Wohnung in ' + details['where'] + ' ab dem ' + details['starts_at']

		return details


	def foo(self):
		return 'foo'