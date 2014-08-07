import util

def main(cmdtext):
	recipient = cmdtext.split(' ')[0]
	message = ' '.join(cmdtext.split(' ')[1:])
	util.sendmsg(recipient, message)