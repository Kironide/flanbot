import flanbot, sys, settings, util.parser, util.misc

bot = flanbot.FlanBot()
while 1:
	for ircsock in bot.ircsocks:
		bot.ircsock = ircsock

		# run periodically repeating functions
		bot.run_repeat()

		# receive data from server
		try:
			ircmsgs = ircsock.recv(settings.recv_data_amount).strip('\r\n').split('\r\n')
		except:
			ircmsgs = []
			continue # if there is no data to read

		for ircmsg in ircmsgs:
			bot.handle_msg(ircmsg)
			p = util.parser.get_parser(ircmsg)

			# write irc messages to a log file
			with open(settings.logfile,'a') as f:
				f.write(ircmsg+'\n')

			try:
				if p.trigger_cmd() and not p.from_self():
					bot.cparser = p

				# check for reload command
				if p.is_command() and p.trigger_reload():
					reload(util)
					reload(settings)
					for util_mod in util.misc.utils_all():
						__import__(util_mod)
						reload(sys.modules[util_mod])
					bot.reply_safe(settings.msg_reload)

				# run events, process commands, etc.
				bot.run_before(ircmsg)
				if p.is_command() and not p.trigger_reload():
					bot.irccommand(p.get_command(), p.get_cmdtext())
				bot.run_after(ircmsg)
			except Exception, e:
				util.misc.handle_exception(e)
				if p.trigger_cmd():
					bot.reply(e)
				continue