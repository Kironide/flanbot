import settings

def main(bot, cmdtext):
	server = bot.serverof[bot.ircsock]
	channels = settings.servers[server]
	for chan in channels:
		bot.join(chan)