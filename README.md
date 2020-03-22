# Flathunter

## Quick Setup
```
sudo apt-get update
sudo apt-get install wget
wget https://github.com/tschuehly/flathunter/archive/master.zip
sudo apt-get install unzip
unzip master.zip
cd flathunter-master
sudo apt-get install python-pip
pip install -r requirements.txt
mv config.yaml.dist config.yaml
nano config.yaml
python flathunter.py
```
## Run Forever

To run flathunter indefinetly:

```
nohup python run_flathunter_forever.py &
```

## Setup


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
                        Config file to use. If not set, try to use
                        '~git-clone-dir/config.yaml'

```

### Configuration

#### Bot registration
A new bot can registered with the telegram chat with the [BotFather](https://telegram.me/BotFather).

#### Chat-Ids
To get the chat id, the [REST-Api](https://core.telegram.org/bots/api) of telegram can be used to fetch the received messages of the Bot.
```
$ curl https://api.telegram.org/bot[BOT-TOKEN]/getUpdates
```

#### Config File

Rename the config.yaml.dist to config.yaml and fill as described.


## Contributers
- [@NodyHub](https://github.com/NodyHub)
- Bene
- [@tschuehly](https://github.com/tschuehly)
- [@Cugu](https://github.com/Cugu)


