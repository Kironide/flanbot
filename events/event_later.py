import util

def main(ircmsg):
	msg = ircmsg.split(' ')
	util.c_mask = msg[0][1:]
	util.c_dtype = msg[1]
	util.c_target = msg[2]

	found = util.later_check(util.current_nick())