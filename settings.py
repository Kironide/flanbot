botnick = 'flanfly'
realname = 'Flandre Scarlet'
prefix = '~'
TEST = True

cmds_secure = ['part','msg','raw']
cmds_disabled = []

prefix_mods = 'mod_'
folder_mods = 'flanmods'

prefix_events = 'event_'
folder_events = 'events'

servers = {}
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy']
	servers['irc.rizon.net'] = ['#flantest','#neritic-net']
	#servers['irc.umich.edu'] = ['#snifit']
else:
	servers['irc.rizon.net'] = ['#flantest']