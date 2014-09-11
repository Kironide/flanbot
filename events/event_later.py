import util, util.later, util.parser

def main(ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.trigger_later():
		util.cparser = p

		messages = util.later.check(util.current_server(), util.current_target(), util.current_nick())
		for message in messages:
			util.reply(message)