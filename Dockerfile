FROM python:3.5.6-alpine3.8

COPY requirements.txt /crawler/

WORKDIR /crawler
RUN pip install -r requirements.txt

COPY config.yaml   /crawler/config.yaml
COPY flathunter    /crawler/flathunter 
COPY flathunter.py /crawler/flathunter.py

ENTRYPOINT python flathunter.py || echo Fooooooooooooooooo


