__author__ = "Jan Harrie"
__license__ = "-/-"
__version__ = "0.2"
__maintainer__ = "Jan Harrie"
__email__ = "harrymcfly@protonmail.com"
__status__ = "Production"

from webscraping import common, xpath
from time import sleep
from unicodedata import normalize

#~ Logging KungFoo
import logging
log = logging.getLogger()

#~ log.addHandler(custom_logger.MyHandler())


class ImmoCrawler:

	def __init__(self, BROWSER_INSTANCE):
		# disable verbose logging from webscraping and define own level
		common.logger.setLevel(logging.CRITICAL)

		# prepare browser
		self.BROWSER=BROWSER_INSTANCE


	def get_results(self, search_url):
		# get html
		html = self.get_page_html(search_url)

		# get number of results
		no_of_results = int(xpath.search(html, '//h1[@class="font-ellipsis font-l font-light font-line-s margin-bottom-none"]/span')[0])
		log.info('search-results: ' + str(no_of_results))

		# get data from first page
		entrys = []
		data = self.extract_data(html)
		entrys.extend(data)
		log.debug('greped: ' + str(len(entrys)))

		# iterat over other pages
		while len(entrys) < no_of_results:
			next_page = xpath.search(html, '//div[@id="pager"]/div[@class="grid-item five-twelfths grid-item-fixed-width align-right"]/a/@href')
			if len(next_page) > 0 :
				log.debug('Next Page')
				next_page = next_page[0]
				next_page = 'https://www.immobilienscout24.de' + str(next_page)
				html = self.get_page_html(next_page)
				data = self.extract_data(html)
				entrys.extend(data)
				log.debug('greped: ' + str(len(entrys)))
			else:
				break

		return entrys


	def get_page_html(self, url):
		self.BROWSER.get(url)
		self.BROWSER.wait(5)
		return self.BROWSER.current_html()



	def extract_data(self, html):
		entrys = []

		# iterat over results
		site_listing = xpath.search(html, '//li[@class="result-list__listing"]')
		for c in site_listing:

			# Summery
			details = {}

			# Get Title
			title = xpath.search(c, '//h5')[0].replace('<!--', '').replace('-->', '').strip()
			if 'span' in title:
				title = title.split('</span>')[1].strip()
			title = normalize('NFKD', title.strip()).encode('ascii','ignore')
			details['title'] = title

			# Get id
			expose_id = xpath.search(c, '//a/@href')[1].strip().split('/')[2]
			details['id'] = int(expose_id)
			details['url'] = 'https://www.immobilienscout24.de/expose/' + str(expose_id)


			# Get Details
			facts = xpath.search(c, '//dd[@class="font-nowrap font-line-xs"]')
			i = 0
			for d in facts:
				# prepare
				if '<span' in d:
					d = d.split('<span')[0]
				d = normalize('NFKD', d.strip()).encode('ascii','ignore')

				# store
				if i is 0:
					details['price'] = d
				if i is 1:
					details['size'] = d
				if i is 2:
					details['rooms'] = d
				# increment
				i = i + 1
			# add to resultset
			entrys.append(details)

		# return result
		log.debug('extracted: ' + str(entrys))
		return entrys


	def foo(self):
		return 'foo'