import util, settings

def main(cmdtext):
	server = util.serverof[util.ircsock]
	channels = settings.servers[server]
	for chan in channels:
		util.joinchan(chan)