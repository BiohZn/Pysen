__author__ = 'BiohZn'

from usercl import ircuser

def init(irc):
	irc.add_privmsg_handler('!auth', auth_handler)
	irc.add_privmsg_handler('!whoami', whoami_handler)
	irc.add_handler('353', names_handler)
	irc.add_handler('354', who_handler)
	irc.add_handler('JOIN', join_handler)
	irc.add_handler('PART', part_handler)
	irc.add_handler('KICK', kick_handler)
	irc.add_handler('QUIT', quit_handler)
	irc.add_handler('NICK', nick_handler)

def kill(irc):
	irc.rem_privmsg_handler('!auth', auth_handler)
	irc.rem_privmsg_handler('!whoami', whoami_handler)
	irc.rem_handler('353', names_handler)
	irc.rem_handler('354', who_handler)
	irc.rem_handler('JOIN', join_handler)
	irc.rem_handler('PART', part_handler)
	irc.rem_handler('KICK', kick_handler)
	irc.rem_handler('QUIT', quit_handler)
	irc.rem_handler('NICK', nick_handler)

def auth_handler(irc, who, sender, params):
	if irc.users[sender['nick']].auth == '0':
		irc.notice(sender['nick'], 'Could not find your auth, trying to fetch it.')
		irc.send("WHO " + sender['nick'] + " n%nuhat,20")

	else:
		irc.notice(sender['nick'], 'You are authed as %s' % irc.users[sender['nick']].auth)

def whoami_handler(irc, who, sender, params):
	if irc.users[sender['nick']].auth == '0':
		irc.notice(sender['nick'], 'Hi %s! We currently have %s common channels, you are not authed and your host is %s' % (irc.users[sender['nick']].nick, str(len(irc.users[sender['nick']].chan)), irc.users[sender['nick']].host))
	else:
		irc.notice(sender['nick'], 'Hi %s! We currently have %s common channels, you are authed as %s and your host is %s' % (irc.users[sender['nick']].nick, str(len(irc.users[sender['nick']].chan)), irc.users[sender['nick']].auth, irc.users[sender['nick']].host))

def names_handler(irc, sender, params):
	chan = params[3]
	users = params[4].replace('@', '').replace('+', '').split(' ')

	for user in users:
		if user not in irc.users:
			irc.users[user] = ircuser(user)

		irc.users[user].chan.add(chan)

	irc.send("WHO " + chan + " n%nuha")

def who_handler(irc, sender, params):
	if params[2] == '20':
		user = params[3]
		host = params[4]
		nick = params[5]
		auth = params[6]

		if nick not in irc.users:
			irc.users[nick] = ircuser(nick)

		irc.users[nick].user = user
		irc.users[nick].host = host
		irc.users[nick].auth = auth

		if auth is not '0':
			irc.notice(nick, 'You are authed as %s' % auth)
		else:
			irc.notice(nick, 'You are not authed')

	else:
		user = params[2]
		host = params[3]
		nick = params[4]
		auth = params[5]

		if nick not in irc.users:
			irc.users[nick] = ircuser(nick)

		irc.users[nick].user = user
		irc.users[nick].host = host
		irc.users[nick].auth = auth

def join_handler(irc, sender, params):
	if sender['nick'] not in irc.users:
		irc.users[sender['nick']] = ircuser(sender['nick'])

	irc.users[sender['nick']].chan.add(params[1])

	if sender['nick'] != irc.config.nick:
		irc.send("WHO " + sender['nick'] + " n%nuha")

def part_handler(irc, sender, params):
	irc.users[sender['nick']].chan.remove(params[1])
	if sender['nick'] != irc.config.nick:
		if len(irc.users[sender['nick']].chan) < 1:
			del(irc.users[sender['nick']])
	else:
		for nick, user in irc.users.items():
			try:
				user.chan.remove(params[1])
			except:
				pass
			if len(user.chan) < 1:
				del(irc.users[user.nick])

def kick_handler(irc, sender, params):
	irc.users[params[2]].chan.remove(params[1])
	if len(irc.users[params[2]].chan) < 1:
		del(irc.users[params[2]])

def quit_handler(irc, sender, params):
	del(irc.users[sender['nick']])

def nick_handler(irc, sender, params):
	print sender['nick']
	print irc.config.nick
	if sender['nick'] == irc.config.nick:
		irc.config.nick = params[1]
		irc.config.write()
	irc.users[params[1]] = irc.users[sender['nick']]
	irc.users[params[1]].nick = params[1]
	del(irc.users[sender['nick']])