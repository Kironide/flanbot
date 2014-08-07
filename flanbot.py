#!/usr/bin/env python

import socket, functions, util, init
from time import sleep

# returns socket connection to IRC server
def get_socket(server, port=6667):
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	util.ircsock = ircsock
	ircsock.connect((server, 6667))
	ircsock.send('USER '+init.botnick+' 0 * :'+init.realname+'\n')
	ircsock.send('NICK '+init.botnick+'\n')
	ircsock.setblocking(0) # very important!!!
	return ircsock

if __name__ == '__main__':
	# start connections to all of the IRC servers in init settings
	ircsocks = []
	serverof = {} # dictionary mapping sock -> server
	for server,channels in init.servers.items():
		ircsock = get_socket(server)
		ircsocks.append(ircsock)
		serverof[ircsock] = server
	util.serverof = serverof
	functions.loaded = False

	# join initial channels
	sleep(3) # wait a bit before joining channels
	for server,channels in init.servers.items():
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
			msg = ircmsg.split(' ')

			nick = util.get_nick(msg[0])

			# stuff that should be performed every time
			functions.run_every_time(msg)

			# runs code for commands starting with init.prefix
			if len(msg) >= 4 and msg[1] == 'PRIVMSG':
				msguser = msg[0][1:]
				msgtype = msg[1]
				msgtarget = msg[2]
				msgtext = ' '.join(msg[3:len(msg)])[1:]

				# give the module the variables
				if nick != init.botnick:
					util.user = msguser
					util.dtype = msgtype
					util.target = msgtarget

				# check for presence of prefix
				try:
					if msgtext[0] == init.prefix:
						cmd = msgtext.split(' ')[0][1:]

						# reload modules
						if cmd == 'reload':
							reload(functions)
							reload(util)
							functions.loaded = False
							util.reply_safe('Reloaded.')

						# create a new socket and add it to the list
						elif cmd == 'server':
							cmdtext = msgtext[1+len(init.prefix)+len(cmd):len(msgtext)]
							ircsock = get_socket(cmdtext)
							ircsocks.append(ircsock)
							serverof[ircsock] = cmdtext
							util.serverof = serverof

						# leaves a server
						elif cmd == 'quit':
							cmdtext = msgtext[1+len(init.prefix)+len(cmd):len(msgtext)]
							if len(cmdtext) == 0:
								try_quit = util.quit()
							else:
								try_quit = util.quit(cmdtext)
							if try_quit:
								ircsocks.remove(ircsock)
								serverof.pop(ircsock,None)
								util.serverof = serverof

						# pass the command over to the functions module
						else:
							cmdtext = msgtext[1+len(init.prefix)+len(cmd):len(msgtext)]
							functions.irccommand(cmd, cmdtext)
				except Exception, e:
					print('Error in flanbot.py.')
					print(e)
					util.reply(e)
					continue

			# reply to server pings
			if ircmsg.find('PING :') != -1:
				ping_msg = ircmsg.split('PING :')
				ping_msg = ping_msg[len(ping_msg)-1].strip()
				util.ping(ping_msg)