#!/usr/bin/env python

"""
to-do list:
- add utility functions for channel and user info
	- add typo correction for user nicks :^)
- finish implementing dice
- think about how to change the settings while the bot is running
- have it keep track of what channels it's a member of on each server
	- maybe just add an event to respond to the channel-joining response
	- and then remove them for parts, kicks, and quits (another event)
- add another event to update channel info
- modify later/seen to use util.dataio
"""

import sys, os, settings, util, util.parser, util.network, util.misc
from time import sleep

if __name__ == '__main__':
	util.ircsocks = []
	util.serverof = {}
	util.loaded = False
	for server,channels in settings.servers.items():
		ircsock = util.network.get_socket(server)
		util.ircsocks.append(ircsock)
		util.serverof[ircsock] = server

	while 1:
		# loop through socket connections indefinitely
		for ircsock in util.ircsocks:
			util.ircsock = ircsock

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