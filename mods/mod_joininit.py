import settings

def main(bot, cmdtext):
	if bot.current_server() in settings.servers:
		for chan in settings.servers[bot.current_server()]:
			bot.join(chan)