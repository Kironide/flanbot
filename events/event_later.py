import util

def main(ircmsg):
	data = ircmsg.split(' ')
	if util.ircmask_valid(data[0]) and (data[1] == 'PRIVMSG' or data[1] == 'JOIN'):
		util.c_mask = data[0][1:]
		util.c_dtype = data[1]
		util.c_target = data[2]

		found = util.later_check(util.current_nick())