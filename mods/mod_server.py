import util

def main(cmdtext):
	ircsock = util.get_socket(cmdtext)
	util.ircsocks.append(ircsock)
	util.serverof[ircsock] = cmdtext