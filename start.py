import flanbot, sys, settings, util.parser, util.misc

bot = flanbot.FlanBot()
while 1:
	bot.next_conn()

	# run periodically repeating functions
	bot.run_repeat()

	# receive data from server and process
	for ircmsg in bot.receive():
		p = bot.handle_msg(ircmsg)
		try:
			if p.trigger_cmd() and not p.from_self():
				bot.cparser = p

			# check for reload command
			if p.is_command() and p.trigger_reload():
				reload(flanbot)
				reload(settings)
				for util_mod in util.misc.utils_all():
					__import__(util_mod)
					reload(sys.modules[util_mod])
				bot = flanbot.copy_bot(bot)
				bot.reply_safe(settings.msg_reload)

			# run events, process commands, etc.
			bot.run_actions(ircmsg, p)
		except Exception, e:
			util.misc.handle_exception(e)
			if p.trigger_cmd():
				bot.reply(e)
			continue