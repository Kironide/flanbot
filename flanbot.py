#!/usr/bin/env python

import sys, settings, util, util.parser, util.network, util.misc
from time import sleep, time

util.init()
for server,channels in settings.servers.items():
	util.misc.exec_cmd(settings.mod_server,server,settings.folder_mods)
while 1:
	for ircsock in util.ircsocks:
		util.ircsock = ircsock

		# run periodically repeating functions
		if time() - util.rtime[ircsock] >= settings.repeat_interval:
			util.rtime[ircsock] = time()
			util.run_repeat()

		# receive data from server
		try:
			ircmsgs = ircsock.recv(settings.recv_data_amount).strip('\r\n').split('\r\n')
		except:
			ircmsgs = []
			continue # if there is no data to read

		for ircmsg in ircmsgs:
			print(ircmsg)
			p = util.parser.get_parser(ircmsg)

			# write irc messages to a log file
			with open(settings.logfile,'a') as f:
				f.write(ircmsg+'\n')

			try:
				# step 1 of 4: check for reload command
				if p.trigger_cmd():
					if not p.from_self():
						util.cparser = p
					if p.is_command() and p.get_command() == 'reload':
						reload(util)
						reload(settings)
						util_modules = util.misc.utils_all()
						for util_mod in util_modules:
							__import__(util_mod)
							reload(sys.modules[util_mod])
						util.loaded = False
						util.reply_safe(settings.msg_reload)

				# step 2 of 3: run pre-command things
				util.run_before(ircmsg)

				# step 3 of 4: run non-reload commands
				if p.trigger_cmd():
					if not p.from_self():
						util.cparser = p
					if p.is_command() and p.get_command() != 'reload':
						util.irccommand(p.get_command(), p.get_cmdtext())

				# step 4 of 4: run post-command things
				util.run_after(ircmsg)

			except Exception, e:
				util.misc.handle_exception(e)
				if p.trigger_cmd():
					util.reply(e)
				continue