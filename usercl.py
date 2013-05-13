# """ IRC User Class """

__author__ = 'BiohZn'

class ircuser:
	def __init__(self, nick):
		self.nick = nick
		self.user = ''
		self.host = ''
		self.auth = ''

		self.chan = set()
