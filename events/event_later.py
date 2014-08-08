import util, util.later, util.parser

def main(ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.trigger_later():
		util.c_mask = p.mask
		util.c_target = p.target

		messages = util.later.later_check(util.current_nick())
		for message in messages:
			util.reply(message)