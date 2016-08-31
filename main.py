#!/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse, os, logging
from webscraping 	import webkit
from foo.immocrawler	import ImmoCrawler
from foo.wgcrawler		import WGGesuchtCrawler
from foo.idmaintainer	import IdMaintainer
from foo.bot_interface	import BotInterface

#~ Logging KungFoo
cyellow = '\033[93m'
cblue = '\033[94m'
coff = '\033[0m'
logging.basicConfig(
		format='[' + cblue + '%(asctime)s' + coff + '|' + cblue + '%(filename)-18s' + coff+ '|' + cyellow + '%(levelname)-8s' + coff + ']: %(message)s',
		datefmt='%Y/%m/%d %H:%M:%S')
log = logging.getLogger(__name__)


def main(args):

	#~ Get Arguments
	BOT_TOKEN = args.BOT_TOKEN
	MY_CHAT_ID = args.USER_ID
	URLs = args.URLs
	VERBOSE = args.verbose

	#~ Logging Kung-Foo
	log.setLevel(logging.DEBUG if VERBOSE else logging.INFO )
	log.info('Start Immoscout Crawler')

	#~ Prepare Database Connection, Crawler and Telegram Bot
	im = IdMaintainer('processed_ids.db')
	BROWSER_INSTANCE = webkit.WebkitBrowser(gui=VERBOSE)
	ic = ImmoCrawler(BROWSER_INSTANCE)
	wgg = WGGesuchtCrawler(BROWSER_INSTANCE)
	bi = BotInterface(BOT_TOKEN)

	#~ Get already messaged exposes
	processed = im.get()
	cnt = 0
	new_links = 0

	#~ Iterate over defined URLs
	URLs.append('wg-gesucht')
	for URL in URLs:

		#~ Trigger crawl of Immoscout
		log.info('Process URL no.#' + str(cnt))
		log.debug(URL)

		if 'wg-gesucht' in URL:
			log.info('Stopped Immoscout Crawler')
			log.debug('Start WG-Gesucht Crawler')
			results = wgg.get_results()
		else:
			results = ic.get_results(URL)

		#~ Iterate over results
		for r in results:

			# check if already processed
			if r['id'] not in processed:
				log.info('New offer: ' + r['title'])
				im.add(r['id'])
				message = r['title'] + '\nZimmer: ' + r['rooms'] + '\nGröße: ' + r['size'] + '\nPreis: ' + r['price'] + '\n' +r['url']

				#~ Send message to telegram user
				bi.send_msg(MY_CHAT_ID,message)
				new_links = new_links + 1
		log.info(str(new_links) + ' new offer found')
		cnt = cnt + 1
	log.info('Stopped WG-Gesucht Crawler')


if __name__ == "__main__":

	parser = argparse.ArgumentParser(
		description='Crawls Immobilienscout24.de and sends results to Telegram User',
		epilog='Designed by Jan Harrie (c) harrymcfly@protonmail.com')

	# Bot Token
	parser.add_argument('BOT_TOKEN', metavar='Bot-Token', type=str, help='The secret token of the Telegram Bot')

	# User ID
	parser.add_argument('USER_ID', metavar='User-ID', type=int, help='ID of the Telegram User')

	# Search URL
	parser.add_argument('URLs', metavar='URL', type=str, nargs='+',
					   help='An URL to Immobilienscout24.de search result')

	# Verbose logging for debug-purpose
	parser.add_argument('-v','--verbose', dest='verbose', action='store_true',
						help='Enable Verbose output')

	args = parser.parse_args()
	main(args)