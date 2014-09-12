import util.seen, util.parser
import time

def main(bot, ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.trigger_seen():
		util.seen.seen_save(time.time(),p.nick,p.dtype,p.target,p.text)