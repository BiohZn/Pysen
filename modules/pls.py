__author__ = 'BiohZn'

def init(irc):
	irc.add_privmsg_handler('pls', pls_handler)
	irc.add_privmsg_handler('lol', lol_handler)

def kill(irc):
	irc.rem_privmsg_handler('pls', pls_handler)
	irc.rem_privmsg_handler('lol', lol_handler)

def pls_handler(irc, who, sender, params):
	irc.msg(who, '%s pls' % sender['nick'])

def lol_handler(irc, who, sender, params):
	irc.msg(who, '%s: Yeah, that was a funny one :D' % sender['nick'])