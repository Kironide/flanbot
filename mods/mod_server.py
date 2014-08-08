import util, util.network

def main(cmdtext):
	ircsock = util.network.get_socket(cmdtext)
	util.ircsocks.append(ircsock)
	util.serverof[ircsock] = cmdtext