# Python Flathunter-Helper

## WTF!?
I coded this stuff while it is horrible to find an appartment in muc!!

## Status
- [X] Telegram Notifier
- [X] Datastorage to store processed IDs
- [X] Immobilienscout24 Crawler
- [ ] WG-Gesucht Crawler
   - [X] Initial Crawler
   - [ ] Definition of Parameter
   - [ ] Optional enble/disable
- [ ] Ebay Kleinanzeigen Crawler


## Required
- Webscraping for Python2.7 (http://bitbucket.org/richardpenman/webscraping)
- Telegram for Python2.7 (https://github.com/liluo/telegram)

**Install:**

	pip2.7 install telegram
	pip2.7 install webscraping

## Usage

	usage: main.py [-h] [-v] Bot-Token User-ID URL [URL ...]

	Crawls Immobilienscout24.de and sends results to Telegram User

	positional arguments:
	  Bot-Token      The secret token of the Telegram Bot
	  User-ID        ID of the Telegram User
	  URL            An URL to Immobilienscout24.de search result

	optional arguments:
	  -h, --help     show this help message and exit
	  -v, --verbose  Enable Verbose output

	Designed by Jan Harrie (c) harrymcfly@protonmail.com

And crawl like a Boss

	while do ./main.py  239_____________________CMtCKSPu7KIhg 1XXXXX090 https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen/-/XXXXXXXXXXXXXXXXX ; echo "sleep 600"; sleep 600;  done