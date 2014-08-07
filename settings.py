botnick = 'flanfly'
realname = 'Flandre Scarlet'
prefix = '~'
servers = {}
TEST = False
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy']
	servers['irc.rizon.net'] = ['#flantest','#neritic-net','#/jp/ma']
	servers['irc.umich.edu'] = ['#snifit']
else:
	servers['irc.rizon.net'] = ['#flantest']

cmds_secure = ['part','msg','raw']
cmds_disabled = []