#!/usr/bin/env python
import sys, settings, util, util.parser, util.misc

util.init()
while 1:
	for ircsock in util.ircsocks:
		util.ircsock = ircsock

		# run periodically repeating functions
		util.run_repeat()

		# receive data from server
		try:
			ircmsgs = ircsock.recv(settings.recv_data_amount).strip('\r\n').split('\r\n')
		except:
			ircmsgs = []
			continue # if there is no data to read

		for ircmsg in ircmsgs:
			util.handle_msg(ircmsg)
			p = util.parser.get_parser(ircmsg)

			# write irc messages to a log file
			with open(settings.logfile,'a') as f:
				f.write(ircmsg+'\n')

			try:
				if p.trigger_cmd() and not p.from_self():
					util.cparser = p

				# check for reload command
				if p.is_command() and p.trigger_reload():
					reload(util)
					reload(settings)
					for util_mod in util.misc.utils_all():
						__import__(util_mod)
						reload(sys.modules[util_mod])
					util.reply_safe(settings.msg_reload)

				# run events, process commands, etc.
				util.run_before(ircmsg)
				if p.is_command() and not p.trigger_reload():
					util.irccommand(p.get_command(), p.get_cmdtext())
				util.run_after(ircmsg)
			except Exception, e:
				util.misc.handle_exception(e)
				if p.trigger_cmd():
					util.reply(e)
				continue