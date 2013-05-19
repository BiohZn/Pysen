""" IRC-Class, parsing server messages, sending to server etc.. """

__author__ = 'BiohZn'

import re
import time
import socket
import platform
from config import cfg
from module import mod
from subprocess import call

class irc:

	connected = False
	users = {}
	handlers = {}
	privmsg_handlers = {}
	hostmask_regex = re.compile('^(.*)!(.*)@(.*)$')

	def __init__(self):
		self.config = cfg()
		self.config.read()
		self.module = mod()

	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.config.host, self.config.port))
		self.send('NICK :%s' % self.config.nick)
		self.send('USER %s * * :%s' % (self.config.user, self.config.real))
		self.module.startup(self)
		self.connected = True

	def add_handler(self, command, handler):
		try:
			self.handlers[command].append(handler)
		except:
			self.handlers[command] = [handler]

	def rem_handler(self, command, handler):
		self.handlers[command].remove(handler)
		if len(self.handlers[command]) == 0:
			del self.handlers[command]

	def add_privmsg_handler(self, command, handler):
		try:
			self.privmsg_handlers[command].append(handler)
		except:
			self.privmsg_handlers[command] = [handler]

	def rem_privmsg_handler(self, command, handler):
		self.privmsg_handlers[command].remove(handler)
		if len(self.privmsg_handlers[command]) == 0:
			del self.privmsg_handlers[command]

	def parser_hostmask(self, hostmask):
		if isinstance(hostmask, dict):
			return hostmask

		nick = None
		user = None
		host = None

		if hostmask is not None:
			match = self.hostmask_regex.match(hostmask)

			if not match:
				nick = hostmask
			else:
				nick = match.group(1)
				user = match.group(2)
				host = match.group(3)

		return {
			'nick': nick,
			'user': user,
			'host': host
		}

	def parse(self, line):
		print "[<] %s" % line

		if line.startswith('ERROR'):
			self.connected = False
			self.module.unload_all(self)
			self.socket.close()
			time.sleep(60.0)
			self.connect()

		else:
			if line[0] == ':':
				sender = self.parser_hostmask(line[1:line.find(' ')])
				command = line[line.find(' ')+1:]
			else:
				sender = 'server'
				command = line

			colonpos = command.find(':')
			if colonpos >= 0:
				params = command[:colonpos-1].split()
				params.append(command[colonpos+1:])
			else:
				params = command.split()

			if params[0].upper() == "PRIVMSG":
				chn = params[1]
				if len(params[2].split()) >= 2:
					cmd = params[2].split()[0]
					prm = params[2].split()[1:]
				else:
					cmd = params[2]
					prm = ''

				try:
					if cmd.lower() == self.config.trigger + 'module':
						self.module_handler(chn, sender, prm)
					for handler in self.privmsg_handlers[cmd.lower()]:
						handler(self, chn, sender, prm)
				except KeyError:
					pass
#					print "[!] PRIVMSG Command not recognized: %s" % cmd

			try:
				for handler in self.handlers[params[0].upper()]:
					handler(self, sender, params)
			except KeyError:
				pass
#				print "[!] Command not recognized: %s" % params[0]

	def send(self, line):
		print "[>] %s" % line
		self.socket.send('%s\r\n' % line)

	def msg(self, to, line):
		self.send('PRIVMSG %s :%s' % (to, line))

	def notice(self, to, line):
		self.send('NOTICE %s :%s' % (to, line))

	def join(self, chan):
		self.send('JOIN %s' % chan)

	def part(self, chan):
		self.send('PART %s' % chan)

	def ctcp(self, to, type, line):
		self.notice(to, '%s%s %s%s' % (chr(1), type, line, chr(1)))

	def module_handler(self, who, sender, params):
		if self.users[sender['nick']].auth in self.config.admins:
			if len(params) == 2:

				if params[0] == 'reload':
					try:
						self.module.reload_module(self, params[1])
						self.notice(sender['nick'], "Module successfully reloaded.")
					except:
						self.notice(sender['nick'], "Module could not be reloaded.")

				elif params[0] == 'unload':
					try:
						self.module.unload_module(self, params[1])
						self.notice(sender['nick'], "Module successfully unloaded.")
					except:
						self.notice(sender['nick'], "Module not found.")

				elif params[0] == 'load':
					try:
						self.module.load_module(self, params[1])
						self.notice(sender['nick'], "Module successfully loaded.")
					except:
						self.notice(sender['nick'], "Module could not be loaded.")
			elif len(params) == 1:
				if params[0] == 'reloadall':
					try:
						self.module.reload_all(self)
						self.notice(sender['nick'], "Modules successfully reloaded.")
					except:
						self.notice(sender['nick'], "Error.")

				elif params[0] == 'update' and platform.system() is not 'Windows':
					call(['git', 'pull'])
					self.module.reload_all(self)
					self.notice(sender['nick'], 'Done.')
			else:
				self.notice(sender['nick'], 'Usage: !module <load/unload> <module>')