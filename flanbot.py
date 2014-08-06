import socket, functions, util, init
from time import sleep

PREFIX = '~'

# returns socket connection to IRC server
def get_socket(server, port=6667):
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	functions.ircsock = ircsock
	ircsock.connect((server, 6667))
	ircsock.send('USER '+init.botnick+' '+init.botnick+' '+init.botnick+' :'+init.realname+'\n')
	ircsock.send('NICK '+init.botnick+'\n')
	ircsock.setblocking(0) # very important!!!
	return ircsock

if __name__ == '__main__':
	# start connections to all of the IRC servers in init settings
	ircsocks = []
	serverof = {} # dictionary mapping sock -> server
	for server,channels in init.servers.items():
		ircsock = get_socket(server)
		sleep(3) # if i join channels too fast it doesn't work sometimes
		for chan in channels:
			functions.joinchan(chan)
		ircsocks.append(ircsock)
		serverof[ircsock] = server
	functions.serverof = serverof
	functions.loaded = False

	while 1:
		# loop through socket connections indefinitely
		for i in range(len(ircsocks)):
			ircsock = ircsocks[i]
			functions.ircsock = ircsock

			# receive data from server
			try:
				ircmsg = ircsock.recv(2048)
			except:
				continue # if there is no data to read
			ircmsg = ircmsg.strip('\n\r')
			print(ircmsg)
			msg = ircmsg.split(' ')
			nick = util.get_nick(msg[0])

			# runs code for commands starting with PREFIX
			if len(msg) >= 4 and msg[1] == 'PRIVMSG':
				msguser = msg[0][1:]
				msgtype = msg[1]
				msgtarget = msg[2]
				msgtext = ' '.join(msg[3:len(msg)])[1:]

				# give the module the variables
				functions.user = msguser
				functions.dtype = msgtype
				functions.target = msgtarget

				# check for presence of prefix
				try:
					if msgtext[0] == PREFIX:
						cmd = msgtext.split(' ')[0][1:]

						# reload modules
						if cmd == 'reload':
							reload(functions)
							reload(util)
							functions.loaded = False
							functions.reply('Reloaded.')

						# create a new socket and add it to the list
						elif cmd == 'server':
							cmdtext = msgtext[1+len(PREFIX)+len(cmd):len(msgtext)]
							ircsock = get_socket(cmdtext)
							ircsocks.append(ircsock)
							serverof[ircsock] = cmdtext
							functions.serverof = serverof

						# leaves a server
						elif cmd == 'quit':
							cmdtext = msgtext[1+len(PREFIX)+len(cmd):len(msgtext)]
							if len(cmdtext) == 0:
								functions.quit()
							else:
								functions.quit(cmdtext)
							ircsocks.remove(ircsock)

						# pass the command over to the functions module
						else:
							cmdtext = msgtext[1+len(PREFIX)+len(cmd):len(msgtext)]
							functions.irccommand(cmd, cmdtext)
				except Exception, e:
					print(e)
					functions.reply(e)
					continue

			# stuff that should be performed every time
			functions.run_every_time(msg)

			# reply to server pings
			if ircmsg.find('PING :') != -1:
				functions.ping()