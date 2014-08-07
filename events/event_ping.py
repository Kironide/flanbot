import util

def main(ircmsg):
	if ircmsg.find('PING :') != -1:
		ping_msg = ircmsg.split('PING :')
		ping_msg = ping_msg[len(ping_msg)-1].strip()
		util.ping(ping_msg)