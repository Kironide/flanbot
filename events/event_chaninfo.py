import util.parser, util.chaninfo

def main(bot, ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.rpl_namreply():
		nicks = p.rpl_namreply_names()
		prefixes = ['@','+','%','~','&']
		for i in range(len(nicks)):
			for prefix in prefixes:
				if nicks[i].startswith(prefix):
					nicks[i] = nicks[i][1:]
		util.chaninfo.add_channel(bot.current_server(),p.rpl_namreply_chan(),nicks)
	elif p.trigger_chaninfo():
		if p.dtype_quit():
			util.chaninfo.remove_nick_serv(bot.current_server(),p.nick)
		elif p.dtype_part():
			util.chaninfo.remove_nick_chan(bot.current_server(),p.target,p.nick)
		elif p.dtype_join():
			util.chaninfo.add_nick_chan(bot.current_server(),p.target,p.nick)