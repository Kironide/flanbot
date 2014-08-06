def main(botnick, server, channels):
	import socket
	import modules, util
	from time import sleep
	pre = '~'

	# load later data
	later = util.get_later()

	channels = channels.split(',')

	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	modules.ircsock = ircsock
	ircsock.connect((server, 6667))
	ircsock.send('USER '+botnick+' '+botnick+' '+botnick+' :test\n')
	ircsock.send('NICK '+botnick+'\n')

	sleep(3) # otherwise sometimes it doesn't work
	for chan in channels:
		modules.joinchan('#'+chan)

	loaded = False

	while 1:
		if not loaded:
			later = util.get_later()

		ircmsg = ircsock.recv(2048)
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
			modules.user = msguser
			modules.dtype = msgtype
			modules.target = msgtarget

			try:
				# check for command with prefix
				if msgtext[0] == pre:
					cmd = msgtext.split(' ')[0][1:]
					if cmd == 'reload':
						reload(modules)
						reload(util)
						modules.reply('Reloaded modules.')
					else:
						cmdtext = msgtext[1+len(pre)+len(cmd):len(msgtext)]
						modules.irccommand(cmd, cmdtext)

			except Exception, e:
				print(e)
				modules.reply(e)
				continue

		# checks for a later message to send upon PRIVMSG or JOIN
		if len(msg) >= 3 and (msg[1] == 'PRIVMSG' or msg[1] == 'JOIN'):
			try:
				modules.user = msg[0][1:]
				modules.dtype = msg[1]
				modules.target = msg[2]

				# sends later messages
				found = modules.check_later(nick, later)
				if found:
					later = util.get_later()
			except Exception, e:
				print(e)
				modules.reply(e)
				continue


		if ircmsg.find('PING :') != -1:
			modules.ping()

def maintest(x):
	while 1:
		print str(x)

if __name__ == '__main__':
	import sys
	main(sys.argv[1],sys.argv[2],sys.argv[3])