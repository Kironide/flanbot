import util, util.network, util.timeutils

def main(cmdtext):
	cmdtext = cmdtext.split(' ')[0]
	ircsock = util.network.get_socket(cmdtext)
	util.ircsocks.append(ircsock)
	util.serverof[ircsock] = cmdtext
	util.rtime[ircsock] = util.timeutils.now()