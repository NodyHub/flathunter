__author__ = "Jan Harrie"
__version__ = "0.2"
__maintainer__ = "Jan Harrie"
__email__ = "harrymcfly@protonmail.com"
__status__ = "Prodction"

from telegram import Bot
import logging

log = logging.getLogger()

class BotInterface:

	def __init__(self, TOKEN):
		log.debug('Create Bot')
		self.BOT_TOKEN = TOKEN
		self.BOT = Bot(self.BOT_TOKEN)

	def send_msg(self, dst, msg):
		log.debug('Send Infos')
		self.BOT.sendMessage(dst, msg)