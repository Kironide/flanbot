import util
import util.seen
import time

def main(ircmsg):
	data = ircmsg.split(' ')
	if len(data) >= 3 and data[1] in ['PRIVMSG','QUIT','PART','JOIN']:
		c_mask = data[0][1:]
		c_dtype = data[1]
		c_target = data[2]
		if c_dtype == 'JOIN':
			c_target = c_target[1:]
		if data[1] == 'PRIVMSG' or data[1] == 'QUIT':
			c_text = ' '.join(data[3:])[1:]
		else:
			c_text = None
		util.seen.seen_save(time.time(), util.ircmask_nick(c_mask),c_dtype,c_target,c_text)