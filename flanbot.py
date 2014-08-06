def main():
	import socket
	import functions, util, init
	from time import sleep
	pre = '~'

	# load data from init.cfg
	botnick = init.botnick
	initservers = init.initservers
	ircsocks = []
	for server,channels in initservers.items():
		ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		functions.ircsock = ircsock
		ircsock.connect((server, 6667))
		ircsock.send('USER '+botnick+' '+botnick+' '+botnick+' :test\n')
		ircsock.send('NICK '+botnick+'\n')
		ircsock.setblocking(0) # THIS IS IMPORTANT!!!

		sleep(3) # if i join channels too fast it doesn't work sometimes
		for chan in channels:
			functions.joinchan(chan)
		ircsocks.append(ircsock)

	# load later data
	later = util.get_later()
	loaded = False

	while 1:
		if not loaded:
			later = util.get_later()

		for i in range(len(ircsocks)):
			ircsock = ircsocks[i]
			functions.ircsock = ircsock
			try:
				ircmsg = ircsock.recv(2048)
			except:
				continue # if there is no data to read
			ircmsg = ircmsg.strip('\n\r')
			print(ircmsg)
			msg = ircmsg.split(' ')
			nick = util.get_nick(msg[0])

			# block to run code for bot commands
			if len(msg) >= 4 and msg[1] == 'PRIVMSG':
				msguser = msg[0][1:]
				msgtype = msg[1]
				msgtarget = msg[2]
				msgtext = ' '.join(msg[3:len(msg)])[1:]

				# give the module the variables
				functions.user = msguser
				functions.dtype = msgtype
				functions.target = msgtarget

				try:
					# check for command with prefix
					if msgtext[0] == pre:
						cmd = msgtext.split(' ')[0][1:]
						if cmd == 'reload':
							reload(functions)
							reload(util)
							functions.reply('Reloaded.')
						else:
							cmdtext = msgtext[1+len(pre)+len(cmd):len(msgtext)]
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


			if ircmsg.find('PING :') != -1:
				functions.ping()

def maintest(x):
	while 1:
		print str(x)

if __name__ == '__main__':
	main()