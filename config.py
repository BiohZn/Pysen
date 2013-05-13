""" Settings for the bot """

__author__ = 'BiohZn'

import ConfigParser

class cfg:
	def __init__(self):
		self.admins = []
		self.chans = []

	def read(self):
		config = ConfigParser.SafeConfigParser()
		config.read('bot.config')

		self.nick = config.get('irc', 'nickname')
		self.user = config.get('irc', 'username')
		self.real = config.get('irc', 'realname')

		self.host = config.get('irc', 'server')
		self.port = config.getint('irc', 'port')

		admins = config.get('irc', 'admins')
		chans = config.get('irc', 'channels')

		for chan in chans.split(','):
			self.chans.append(chan)

		for admin in admins.split(','):
			self.admins.append(admin)

	def write(self):
		chans = ','.join(self.chans)
		admins = ','.join(self.admins)

		config = ConfigParser.RawConfigParser()
		config.read('bot.config')
		config.set('irc', 'channels', chans)
		config.set('irc', 'admins', admins)

		with open('bot.config', 'wb') as configfile:
			config.write(configfile)