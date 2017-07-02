import urllib
import requests
import logging
from flathunter.sender_base import SenderBase as Base


class SenderTelegram(Base):
    __log__ = logging.getLogger(__name__)

    def __init__(self, cfg):
        self.cfg = cfg
        self.bot_token = self.cfg.get('telegram', dict()).get('bot_token', '')
        self.receiver_ids = self.cfg.get('telegram', dict()).get('receiver_ids', list())


    def send_msg(self, message):
        for chat_id in self.receiver_ids:
            url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%i&text=%s'
            text = urllib.parse.quote_plus(message.encode('utf-8'))
            qry = url % (self.bot_token, chat_id, text)
            self.__log__.debug("Retrieving URL %s" % qry)
            resp = requests.get(qry)
            self.__log__.debug("Got response (%i): %s" % (resp.status_code, resp.content))
            data = resp.json()

            # handle error
            if resp.status_code != 200:
                sc = resp.status_code
                self.__log__.error("When sending bot message, we got status %i with message: %s" % (sc, data))
