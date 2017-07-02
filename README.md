# Python Flathunter-Helper

## Setup

### Virtual Environment
Install 
```
$ pip install virtualenv
```

Swith in project directory and create a virtual environment
```
$ virtualenv -p /usr/bin/python3.6 venv
```

Activate virtual environment
```
$ source venv/bin/activate
```


### Requirements
Install requirements (with acvtivated venv)
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