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

Example Output

	$ ./main.py -v 239_____________________CMtCKSPu7KIhg 1XXXXX090 https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen/-/XXXXXXXXXXXXXXXXXg
	[2016/08/31 21:58:40|main.py           |INFO    ]: Start Immoscout Crawler
	[2016/08/31 21:58:40|main.py           |INFO    ]: Process URL no.#0
	[2016/08/31 21:58:40|main.py           |DEBUG   ]: https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen/-/XXXXXXXXXXXXXXXXXg
	[2016/08/31 21:58:50|main.py           |INFO    ]: 0 new offer found
	[2016/08/31 21:58:50|main.py           |INFO    ]: Process URL no.#1
	[2016/08/31 21:58:50|main.py           |DEBUG   ]: wg-gesucht
	[2016/08/31 21:58:50|main.py           |INFO    ]: Stopped Immoscout Crawler
	[2016/08/31 21:58:50|main.py           |DEBUG   ]: Start WG-Gesucht Crawler
	[2016/08/31 21:59:04|main.py           |INFO    ]: 0 new offer found
	[2016/08/31 21:59:04|main.py           |INFO    ]: Stopped WG-Gesucht Crawler


And crawl like a Boss

	$ while do ./main.py  239_____________________CMtCKSPu7KIhg 1XXXXX090 https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Bayern/Muenchen/-/XXXXXXXXXXXXXXXXXg ; echo "sleep 600"; sleep 600;  done
	
	
Test Code Highlight
<pre>
Foo1 <b>Bar</b> Test
</pre>	
