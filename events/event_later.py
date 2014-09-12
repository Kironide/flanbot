import util.later, util.parser

def main(bot, ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.trigger_later():
		bot.cparser = p

		messages = util.later.check(bot.current_server(), bot.current_target(), bot.current_nick())
		for message in messages:
			bot.reply(message)