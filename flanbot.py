import socket, functions, util, init
from time import sleep

PREFIX = '~'

# returns socket connection to IRC server
def get_socket(server, port=6667):
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	functions.ircsock = ircsock
	ircsock.connect((server, 6667))
	ircsock.send('USER '+init.botnick+' '+init.botnick+' '+init.botnick+' :Flandre\n')
	ircsock.send('NICK '+init.botnick+'\n')
	ircsock.setblocking(0) # very important!!!
	return ircsock

if __name__ == '__main__':
	# start connections to all of the IRC servers in init settings
	ircsocks = []
	for server,channels in init.servers.items():
		ircsock = get_socket(server)
		sleep(3) # if i join channels too fast it doesn't work sometimes
		for chan in channels:
			functions.joinchan(chan)
		ircsocks.append(ircsock)

	# load data for the 'later' command
	later = util.get_later()
	loaded = False

	while 1:
		# reload the data for the 'later' command
		# I don't know why this is necessary
		if not loaded:
			later = util.get_later()

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
							functions.reply('Reloaded.')

						# create a new socket and add it to the list
						elif cmd == 'server':
							cmdtext = msgtext[1+len(PREFIX)+len(cmd):len(msgtext)]
							ircsocket = get_socket(cmdtext)
							ircsocks.append(ircsocket)

						# pass the command over to the functions module
						else:
							cmdtext = msgtext[1+len(PREFIX)+len(cmd):len(msgtext)]
							functions.irccommand(cmd, cmdtext)
				except Exception, e:
					print(e)
					functions.reply(e)
					continue

			# checks for a later message to send upon PRIVMSG or JOIN
			if len(msg) >= 3 and (msg[1] == 'PRIVMSG' or msg[1] == 'JOIN'):
				try:
					functions.user = msg[0][1:]
					functions.dtype = msg[1]
					functions.target = msg[2]

					# sends later messages
					found = functions.check_later(nick, later)
					if found:
						later = util.get_later()
				except Exception, e:
					print(e)
					functions.reply(e)
					continue

			# reply to server pings
			if ircmsg.find('PING :') != -1:
				functions.ping()