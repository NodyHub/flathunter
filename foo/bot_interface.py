# -*- coding: utf-8 -*-

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