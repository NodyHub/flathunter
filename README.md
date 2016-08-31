# py_flathunt

## WTF!?
I coded this stuff while it's fucking horrible to find an appartment in muc!! 

## Status
[X] Telegram Notifier
[X] Datastorage to store processed IDs
[X] Immobilienscout24 Crawler
[X] WG-Gesucht Crawler
[ ] Ebay kleinanzeigen Crawler

## Required
Telegram for python2.7 (https://github.com/liluo/telegram)

   pip2.7 install telegram

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

