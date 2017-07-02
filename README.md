# Python Flathunter-Helper

## Setup

### Virtual Environment (Optional)
To keep you python requirements clean, it is recommended to run the
-project in a virtual environment. Install ```virtualenv```, create a
venv and activate
```
$ pip install virtualenv
$ virtualenv -p /usr/bin/python3.6 venv
$ source venv/bin/activate
```


### Requirements
Install requirements from ```requirements.txt``` to run execute flathunter properly.
```
pip install -r requirements.txt
```

## Usage
```
usage: flathunter.py [-h] [--config CONFIG]

Searches for flats on Immobilienscout24.de and wg-gesucht.de and sends results
to Telegram User

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Config file to use. If not set, $PROJECT_DIR/config.yaml is used.
```

## Contributers
- [@NodyHub](https://github.com/NodyHub)
- Bene
- [@Cugu](https://github.com/Cugu)