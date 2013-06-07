#!/usr/bin/python

""" Main Class for the Bot """

__author__ = 'BiohZn'

import sys
sys.dont_write_bytecode = True

from irccon import irc

class main:
	def __init__(self):
		self.buffer = ''
		self.irc = irc()

	def connect(self):
		self.irc.connect()

	def read(self):
		self.buffer += self.irc.socket.recv(8192)
		while self.buffer.find('\r\n') != -1:
			currentline = self.buffer.split('\r\n')[0]
			self.buffer = self.buffer[len(currentline)+2:]
			self.irc.parse(currentline)

if __name__ == '__main__':
	bot = main()
	bot.connect()
	while 1:
		if bot.irc.connected:
			bot.read()
