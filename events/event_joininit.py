import util, util.parser
import settings

def main(ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.rpl_welcome():
		if util.current_server() in settings.servers:
			for chan in settings.servers[util.current_server()]:
				util.joinchan(chan)