import util.parser
import settings

def main(bot, ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.rpl_welcome():
		if bot.current_server() in settings.servers:
			for chan in settings.servers[bot.current_server()]:
				bot.join(chan)