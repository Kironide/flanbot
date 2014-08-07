botnick = 'flanfly'
realname = 'Flandre Scarlet'
prefix = '~'
prefix_mods = 'mod_'
folder_mods = 'flanmods'
servers = {}
TEST = False
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy']
	servers['irc.rizon.net'] = ['#flantest','#neritic-net']
	servers['irc.umich.edu'] = ['#snifit']
else:
	servers['irc.rizon.net'] = ['#flantest']

cmds_secure = ['part','msg','raw']
cmds_disabled = []