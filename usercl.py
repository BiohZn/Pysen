#!/usr/bin/python

""" IRC User Class """

class ircuser:
	def __init__(self, nick):
		self.nick = nick
		self.user = ''
		self.host = ''
		self.auth = ''

		self.chan = set()
