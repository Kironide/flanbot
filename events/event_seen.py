import util

def main(ircmsg):
	data = ircmsg.split(' ')
	if len(data) >= 3 and data[1] in ['PRIVMSG','QUIT','PART','JOIN']:
		util.c_mask = data[0][1:]
		util.c_dtype = data[1]
		util.c_target = data[2]