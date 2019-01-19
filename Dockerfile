FROM python:3.5.6-alpine3.8

COPY . /crawler/

WORKDIR /crawler

RUN pip install -r requirements.txt

ENTRYPOINT python flathunter.py || echo Fooooooooooooooooo


