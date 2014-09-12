import util.parser
import settings

def main(bot, ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.err_nicknameinuse():
		bot.change_nick(p.err_nicknameinuse_nick()+settings.nick_ext)