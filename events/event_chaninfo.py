import util, util.parser, util.chaninfo

def main(ircmsg):
	p = util.parser.get_parser(ircmsg)
	if p.rpl_namreply():
		nicks = p.rpl_namreply_names()
		prefixes = ['@','+','%','~','&']
		for i in range(len(nicks)):
			for prefix in prefixes:
				if nicks[i].startswith(prefix):
					nicks[i] = nicks[i][1:]
		util.chaninfo.add_channel(util.current_server(),p.rpl_namreply_chan(),nicks)
	elif p.trigger_chaninfo():
		if p.dtype == 'QUIT':
			util.chaninfo.remove_nick_serv(util.current_server(),p.nick)
		elif p.dtype == 'PART':
			util.chaninfo.remove_nick_chan(util.current_server(),p.target,p.nick)
		elif p.dtype == 'JOIN':
			util.chaninfo.add_nick_chan(util.current_server(),p.target,p.nick)