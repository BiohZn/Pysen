__author__ = 'BiohZn'

def init(irc):
	irc.add_privmsg_handler(irc.config.trigger + 'mode', channel_mode_handler)
	irc.add_privmsg_handler(irc.config.trigger + 'topic', channel_topic_handler)

def kill(irc):
	irc.rem_privmsg_handler(irc.config.trigger + 'mode', channel_mode_handler)
	irc.rem_privmsg_handler(irc.config.trigger + 'topic', channel_topic_handler)

def channel_mode_handler(irc, who, sender, params):
	if irc.users[sender['nick']].auth in irc.config.admins:
		if len(params) > 1:
			if params[0] == 'op':
				m = ''
				for a in params[1:]:
					m += 'o'
				irc.send('MODE %s +%s %s' % (who, m, ' '.join(params[1:])))

			elif params[0] == 'deop':
				m = ''
				for a in params[1:]:
					m += 'o'
				irc.send('MODE %s -%s %s' % (who, m, ' '.join(params[1:])))

			elif params[0] == 'op':
				m = ''
				for a in params[1:]:
					m += 'v'
				irc.send('MODE %s +%s %s' % (who, m, ' '.join(params[1:])))

			elif params[0] == 'devoice':
				m = ''
				for a in params[1:]:
					m += 'v'
				irc.send('MODE %s -%s %s' % (who, m, ' '.join(params[1:])))

		else:
			irc.notice(sender['nick'], 'Usage: !mode <op/voice> <nicklist>')

def channel_topic_handler(irc, who, sender, params):
	if irc.users[sender['nick']].auth in irc.config.admins:
		if len(params) > 0:
			irc.send('TOPIC %s :%s' % (who, ' '.join(params)))