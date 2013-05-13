""" Module manager """

__author__ = 'BiohZn'

import os
import sys

class mod:
	modules_dir = 'modules'
	sys.path.append(modules_dir)
	modules = {}

	def __init__(self):
		pass

	def loaded_module(self, irc, module):
		if module in self.modules: return True
		else: return False

	def load_module(self, irc, module):
		if not self.loaded_module(irc, module):
			print "[+] Loading module: %s" % module
			mod = __import__(module)
			self.modules[module] = mod
			mod.init(irc)
		else:
			print "[!] Module already loaded: %s" % module

	def unload_module(self, irc, module):
		if self.loaded_module(irc, module):
			print "[-] Unloading module: %s" % module
			self.modules[module].kill(irc)
			del self.modules[module]
		else:
			print "[!] Module not loaded: %s" % module

	def reload_module(self, irc, module):
		print "[!] Reloading module: %s" % module
		try:
			self.modules[module].reloading(irc)
		except:
			self.modules[module].kill(irc)

		reload(self.modules[module])

		try:
			self.modules[module].reloaded(irc)
		except:
			self.modules[module].init(irc)

	def startup(self, irc):
		print "[!] Loading startup modules"
		for module in os.listdir(self.modules_dir):
			if module[-3:] == '.py':
				self.load_module(irc, module[:-3])

	def reload_all(self, irc):
		print "[!] Reloading all modules"
		for module in self.modules.keys():
			self.reload_module(irc, module)

	def unload_all(self, irc):
		print "[!] Unloading all modules"
		for module in self.modules.keys():
			self.unload_module(irc, module)

