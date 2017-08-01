# Flathunter

A python crawler which crawls Immobilienscout24.de and wg-gesucht.de for new appartments and sends the results to a Telegram user

## Setup

Install requirements from ```requirements.txt``` to run execute flathunter properly.
```
pip install -r requirements.txt
```

Rename ```config.yaml.dist``` to ```config.yaml``` and go through it to adapt it to your needs.

## Usage
```
usage: flathunter.py [-h] [--config CONFIG]

Searches for flats on Immobilienscout24.de and wg-gesucht.de and sends results
to Telegram User

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Config file to use. If not set, try to use
                        '~git-clone-dir/config.yaml'

```

## Contributers
- [@NodyHub](https://github.com/NodyHub)
- Bene
- [@Cugu](https://github.com/Cugu)


