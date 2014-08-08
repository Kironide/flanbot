#!/usr/bin/env python

"""
to-do list:
- add utility functions for channel and user info
- finish implementing dice
- think about how to change the settings while the bot is running
"""

import sys, os, settings, util, util.parser, util.network
from time import sleep

if __name__ == '__main__':
	util.ircsocks = []
	nick_ext, first_loop, serverof = {}, {}, {}
	for server,channels in settings.servers.items():
		ircsock = util.network.get_socket(server)
		util.ircsocks.append(ircsock)
		serverof[ircsock] = server
		nick_ext[ircsock] = ''
		first_loop[ircsock] = True
	util.serverof = serverof
	util.loaded = False

	sleep(3)

	while 1:
		# loop through socket connections indefinitely
		for sock in util.ircsocks:
			util.ircsock = sock
			ircsock = sock

			# receive data from server
			try:
				ircmsg = ircsock.recv(2048)
			except:
				ircmsg = ''
				continue # if there is no data to read
			ircmsg = ircmsg.strip('\r\n')
			ircmsgs = ircmsg.split('\r\n')

			for ircmsg in ircmsgs:
				print(ircmsg)
				p = util.parser.get_parser(ircmsg)

				# write irc messages to a log file
				with open(settings.logfile,'a') as f:
					f.write(ircmsg+'\n')

				# if it's the first loop then do some stuff
				if ircsock in first_loop and first_loop[ircsock]:
					channels = settings.servers[util.serverof[ircsock]]
					for chan in channels:
						util.joinchan(chan)
					first_loop[ircsock] = False

				# change nick if there's a conflict
				if p.err_nicknameinuse():
					nick_ext[ircsock] += '_'
					ircsock.send('NICK '+settings.botnick+nick_ext[ircsock]+'\n')
					if ircsock in first_loop:
						first_loop[ircsock] = True

				try:
					# checks for reload
					if p.trigger_cmd():
						if not p.from_self():
							util.cparser = p
						if p.is_command() and p.get_command() == 'reload':
							reload(util)
							reload(settings)
							util_modules = ['util.'+x.replace('.py','') for x in os.listdir('util/') if x.endswith('.py') and x != '__init__.py']
							for util_mod in util_modules:
								__import__(util_mod)
								reload(sys.modules[util_mod])
							util.loaded = False
							util.reply_safe(settings.msg_reload)

					util.run_before(ircmsg)

					# runs code for commands starting with settings.prefix
					if p.trigger_cmd():
						if not p.from_self():
							util.cparser = p
						if p.is_command() and p.get_command != 'reload':
							util.irccommand(p.get_command(), p.get_cmdtext(), sock=ircsock)

					util.run_after(ircmsg)
				except Exception, e:
					util.handle_exception(e)
					if p.trigger_cmd():
						util.reply(e)