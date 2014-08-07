#!/usr/bin/env python

import socket, util, settings, sys, os
from time import sleep

# returns socket connection to IRC server
def get_socket(server, port=6667):
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	util.ircsock = ircsock
	ircsock.connect((server, 6667))
	ircsock.send('USER '+settings.botnick+' 0 * :'+settings.realname+'\n')
	ircsock.send('NICK '+settings.botnick+'\n')
	ircsock.setblocking(0) # very important!!!
	return ircsock

if __name__ == '__main__':
	# start connections to all of the IRC servers in settings
	ircsocks = []
	serverof = {} # dictionary mapping sock -> server
	for server,channels in settings.servers.items():
		ircsock = get_socket(server)
		ircsocks.append(ircsock)
		serverof[ircsock] = server
	util.serverof = serverof
	util.loaded = False

	# join initial channels
	sleep(3) # wait a bit before joining channels
	for server,channels in settings.servers.items():
		for ircsock in ircsocks:
			if serverof[ircsock] == server:
				util.ircsock = ircsock
				for chan in channels:
					util.joinchan(chan)

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
			ircmsg = ircmsg.strip('\n\r')
			print(ircmsg)

			# write irc messages to a log file
			with open(settings.logfile,'a') as f:
				f.write(ircmsg+'\n')

			# stuff that should be performed every time
			util.run_before(ircmsg)

			# runs code for commands starting with settings.prefix
			data = ircmsg.split(' ')
			if util.ircmask_valid(data[0]) and data[1] == 'PRIVMSG':
				c_mask = data[0][1:]
				c_dtype = data[1]
				c_target = data[2]
				c_text = ' '.join(data[3:len(data)])[1:]

				nick = util.ircmask_nick(c_mask)

				# give the module the variables
				if nick != settings.botnick:
					util.c_mask = c_mask
					util.c_dtype = c_dtype
					util.c_target = c_target

				# check for presence of prefix
				try:
					if c_text[0] == settings.prefix:
						cmd = c_text.split(' ')[0][1:]

						# reload modules
						if cmd == 'reload':
							reload(util)
							reload(settings)
							util_modules = ['util.'+x.replace('.py','') for x in os.listdir('util/') if x.endswith('.py') and x != '__init__.py']
							for util_mod in util_modules:
								__import__(util_mod)
								reload(sys.modules[util_mod])
							util.loaded = False
							util.reply_safe('Reloaded.')

						# create a new socket and add it to the list
						elif cmd == 'server':
							cmdtext = c_text[1+len(settings.prefix)+len(cmd):len(c_text)]
							ircsock = get_socket(cmdtext)
							ircsocks.append(ircsock)
							serverof[ircsock] = cmdtext
							util.serverof = serverof

						# leaves a server
						elif cmd == 'quit':
							cmdtext = c_text[1+len(settings.prefix)+len(cmd):len(c_text)]
							if len(cmdtext) == 0:
								try_quit = util.quit()
							else:
								try_quit = util.quit(cmdtext)
							if try_quit:
								ircsocks.remove(ircsock)
								serverof.pop(ircsock,None)
								util.serverof = serverof

						# pass the command over
						else:
							cmdtext = c_text[1+len(settings.prefix)+len(cmd):len(c_text)]
							util.irccommand(cmd, cmdtext, sock=ircsock)

				except Exception, e:
					print('Encountered an exception.')
					print(e)
					util.reply(e)
					continue

			util.run_after(ircmsg)