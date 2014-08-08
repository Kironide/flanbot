# utility functions that relate to networking
# uses the inbuilt 'socket' package

import socket, settings

# returns socket connection to IRC server
def get_socket(server, port=6667):
	ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ircsock.connect((server, 6667))
	ircsock.send('USER '+settings.botnick+' 0 * :'+settings.realname+'\n')
	ircsock.send('NICK '+settings.botnick+'\n')
	ircsock.setblocking(0) # very important!!!
	return ircsock