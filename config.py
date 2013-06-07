""" Settings for the bot """

__author__ = 'BiohZn'

import ConfigParser

class cfg:
	config = ConfigParser.SafeConfigParser()
	admins = []
	chans = []


	def __init__(self):
		self.__dict__['admins'] = []
		self.__dict__['chans'] = []
		self.__dict__['config'] = ConfigParser.SafeConfigParser()
		self.config.read('bot.config')

		admins = self.config.get('irc', 'admins')
		chans = self.config.get('irc', 'channels')
		for chan in chans.split(','):
			self.chans.append(chan)
		for admin in admins.split(','):
			self.admins.append(admin)


	def __getattr__(self, key):
		return self.config.get('irc', key)

	def __setattr__(self, key, value):
		self.config.set('irc', key, value)

	def write(self):
		chans = ','.join(self.chans)
		admins = ','.join(self.admins)

		with open('bot.config', 'wb') as configfile:
			self.config.write(configfile)
	def __del__(self):
		self.write()
