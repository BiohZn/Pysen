from usercl import ircuser

def init(irc):
	irc.add_privmsg_handler(chr(1) + 'version' + chr(1), version_handler)
	irc.add_privmsg_handler('!module', module_handler)
	irc.add_privmsg_handler('!channel', channel_handler)
	irc.add_privmsg_handler('!admin', admin_handler)
	irc.add_privmsg_handler('!users', users_handler)
	irc.add_handler('001', welcome_handler)
	irc.add_handler('433', name_in_use_handler)
	irc.add_handler('PING', ping_handler)
	irc.add_handler('JOIN', core_join_handler)
	irc.add_handler('PART', core_part_handler)

def kill(irc):
	irc.rem_privmsg_handler(chr(1) + 'version' + chr(1), version_handler)
	irc.rem_privmsg_handler('!module', module_handler)
	irc.rem_privmsg_handler('!channel', channel_handler)
	irc.rem_privmsg_handler('!admin', admin_handler)
	irc.rem_privmsg_handler('!users', users_handler)
	irc.rem_handler('001', welcome_handler)
	irc.rem_handler('433', name_in_use_handler)
	irc.rem_handler('PING', ping_handler)
	irc.rem_handler('JOIN', core_join_handler)
	irc.rem_handler('PART', core_part_handler)

def version_handler(irc, who, sender, params):
	irc.ctcp(sender['nick'], 'VERSION', 'Pysen v0.1')

def module_handler(irc, who, sender, params):
	if irc.users[sender['nick']].auth in irc.config.admins:
		if len(params) == 2:
			if params[0] == 'reload':
				try:
					irc.module.reload_module(irc, params[1])
					irc.notice(sender['nick'], "Module successfully reloaded.")
				except:
					irc.notice(sender['nick'], "Module not found.")

			if params[0] == 'unload':
				try:
					irc.module.unload_module(irc, params[1])
					irc.notice(sender['nick'], "Module successfully unloaded.")
				except:
					irc.notice(sender['nick'], "Module not found.")

			if params[0] == 'load':
				try:
					irc.module.load_module(irc, params[1])
					irc.notice(sender['nick'], "Module successfully loaded.")
				except:
					irc.notice(sender['nick'], "Module could not be loaded.")
		else:
			irc.notice(sender['nick'], 'Usage: !module <load/unload> <module>')

def channel_handler (irc, who, sender, params):
	if irc.users[sender['nick']].auth in irc.config.admins:
		if len(params) > 1:
			if params[0] == 'join':
				if params[1][0] != '#': params[1] = '#%s' % params[1]
				if params[1] not in irc.config.chans:
					irc.join(params[1])
					irc.notice(sender['nick'], 'Joining %s' % params[1])
				else:
					irc.notice(sender['nick'], 'I\'m already in %s' % params[1])

			elif params[0] == 'part':
				if params[1][0] != '#': params[1] = '#%s' % params[1]
				if params[1] in irc.config.chans:
					irc.part(params[1])
					irc.notice(sender['nick'], 'Parting %s' % params[1])
				else:
					irc.notice(sender['nick'], 'I\'m not in %s' % params[1])

		if len(params) > 0:
			if params[0] == 'list':
				channels = ' | '.join(irc.config.chans)
				irc.notice(sender['nick'], '%s | END OF LIST' % channels)
		else:
			irc.notice(sender['nick'], 'Usage: !channel <join/part> #channel')

def admin_handler (irc, who, sender, params):
	if irc.users[sender['nick']].auth in irc.config.admins:
		if len(params) > 1:
			if params[0] == 'add':
				if params[1][0] == '#': auth = params[1][1:]
				else:
					try:
						auth = irc.users[params[1]].auth
					except:
						auth = '0'

				if auth is not '0':
					if auth not in irc.config.admins:
						irc.config.admins.append(auth)
						irc.notice(sender['nick'], 'Admin added')
						irc.config.write()
					else:
						irc.notice(sender['nick'], 'User is an admin')
				else:
					irc.notice(sender['nick'], 'User is not authed or i cant find the user')

			if params[0] == 'del':
				if params[1][0] == '#': auth = params[1][1:]
				else:
					try:
						auth = irc.users[params[1]].auth
					except:
						auth = '0'

				if auth is not '0':
					if auth in irc.config.admins:
						irc.config.admins.remove(auth)
						irc.notice(sender['nick'], 'Admin removed')
						irc.config.write()
					else:
						irc.notice(sender['nick'], 'User is not an admin')
				else:
					irc.notice(sender['nick'], 'User is not authed or i cant find the user')

		if len(params) > 0:
			if params[0] == 'list':
				admins = ' | '.join(irc.config.admins)
				irc.notice(sender['nick'], '%s | END OF LIST' % admins)

def users_handler(irc, who, sender, params):
	if irc.users[sender['nick']].auth in irc.config.admins:
		irc.notice(sender['nick'], 'I currently know %s users.' % len(irc.users))

def name_in_use_handler(irc, sender, params):
	nick = "%s_" % irc.config.nick
	irc.config.nick = nick
	irc.send('NICK :%s' % nick)

def ping_handler(irc, sender, params):
	if params[0] == 'PING':
		irc.send('PONG :%s' % params[1])

def welcome_handler(irc, sender, params):
	for channel in irc.config.chans:
		irc.join(channel)

def core_join_handler(irc, sender, params):
	if sender['nick'] == irc.config.nick:
		if params[1].lower() not in irc.config.chans:
			irc.config.chans.append(params[1].lower())
		irc.config.write()

def core_part_handler(irc, sender, params):
	if sender['nick'] == irc.config.nick:
		try:
			irc.config.chans.remove(params[1].lower())
		except:
			pass
		irc.config.write()