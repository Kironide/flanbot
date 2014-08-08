#!/usr/bin/env python

"""
to-do list:
- improve server, quit commands
- add utility functions for channel and user info
"""

import socket, sys, os, settings, util, util.parser
from time import sleep

# returns socket connection to IRC server
def get_socket(server, port=6667):
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ircsock.connect((server, 6667))
	ircsock.send('USER '+settings.botnick+' 0 * :'+settings.realname+'\n')
	ircsock.send('NICK '+settings.botnick+'\n')
	ircsock.setblocking(0) # very important!!!
	return ircsock

if __name__ == '__main__':
	ircsocks = []
	nick_ext = {}
	first_loop = {}
	serverof = {} # dictionary mapping sock -> server
	for server,channels in settings.servers.items():
		ircsock = get_socket(server)
		ircsocks.append(ircsock)
		serverof[ircsock] = server
		nick_ext[ircsock] = ''
		first_loop[ircsock] = True
	util.serverof = serverof
	util.loaded = False

	sleep(3)

	while 1:
		# loop through socket connections indefinitely
		for i in range(len(ircsocks)):
			ircsock = ircsocks[i]
			util.ircsock = ircsock

			# receive data from server
			try:
				ircmsg = ircsock.recv(2048)
			except:
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
					channels = settings.servers[serverof[ircsock]]
					for chan in channels:
						util.joinchan(chan)
					first_loop[ircsock] = False

				# change nick if there's a conflict
				if p.err_nicknameinuse():
					nick_ext[ircsock] += '_'
					ircsock.send('NICK '+settings.botnick+nick_ext[ircsock]+'\n')
					if ircsock in first_loop:
						first_loop[ircsock] = True

				# checks for reload
				if p.trigger_cmd():
					if not p.from_self():
						util.c_mask,util.c_target = p.mask,p.target
					if p.is_command() and p.get_command() == 'reload':
						try:
							reload(util)
							reload(settings)
							util_modules = ['util.'+x.replace('.py','') for x in os.listdir('util/') if x.endswith('.py') and x != '__init__.py']
							for util_mod in util_modules:
								__import__(util_mod)
								reload(sys.modules[util_mod])
							util.loaded = False
							util.reply_safe(settings.msg_reload)
						except Exception, e:
							print('Error detected while reloading.')
							print(e)
							util.reply(e)
							continue

				# stuff that should be performed every time
				try:
					util.run_before(ircmsg)
				except Exception, e:
					print('Error detected in util.run_before().')
					print(e)
					continue

				# runs code for commands starting with settings.prefix
				if p.trigger_cmd():
					if not p.from_self():
						util.c_mask,util.c_target = p.mask,p.target
					if p.is_command():
						cmd,cmdtext = p.get_command(),p.get_cmdtext()

						# create a new socket and add it to the list
						if cmd == 'server':
							if util.auth():
								ircsock = get_socket(cmdtext)
								ircsocks.append(ircsock)
								serverof[ircsock] = cmdtext
								util.serverof = serverof
							else:
								util.reply(settings.msg_notauth)

						# leaves a server
						elif cmd == 'quit':
							if util.auth():
								if len(cmdtext) == 0:
									try_quit = util.quit()
								else:
									try_quit = util.quit(cmdtext)
								if try_quit:
									ircsocks.remove(ircsock)
									serverof.pop(ircsock,None)
									util.serverof = serverof
							else:
								util.reply(settings.msg_notauth)

						# pass the command over
						elif cmd != 'reload':
							try:
								util.irccommand(cmd, cmdtext, sock=ircsock)
							except Exception, e:
								print('Error detected in util.irccommand().')
								print(e)
								util.reply(e)
								continue

				try:
					util.run_after(ircmsg)
				except Exception, e:
					print('Error detected in util.run_after().')
					print(e)
					continue