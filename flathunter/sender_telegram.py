import urllib
import requests
import logging
from flathunter.sender_base import SenderBase as Base


class SenderTelegram(Base):
    __log__ = logging.getLogger(__name__)

    def __init__(self, cfg):
        self.cfg = cfg

    def send_msg(self, bot_token, chat_id, message):
        url = 'https://api.telegram.org/%s/sendMessage?chat_id=%i&text=%s'
        text = urllib.parse.quote_plus(message.encode('utf-8'))
        qry = url % (bot_token, chat_id, text)
        self.__log__.debug("Retrieving URL %s" % qry)
        resp = requests.get(qry)
        self.__log__.debug("Got response (%i): %s" % (resp.status_code, resp.content))
        data = resp.json()

        # handle error
        if resp.status_code != 200:
            sc = resp.status_code
            self.__log__.error("When sending bot message, we got status %i with message: %s" % (sc, data))
