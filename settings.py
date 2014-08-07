botnick = 'flanfly'
realname = 'Flandre Scarlet'
prefix = '~'
logfile = 'flanlog.log'
TEST = False

cmds_secure = ['part','msg','raw']
cmds_disabled = []

prefix_mods = 'mod_'
folder_mods = 'mods'

prefix_events = 'event_'
folder_events = 'events'

servers = {}
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy']
	servers['irc.rizon.io'] = ['#flantest','#neritic-net']
	servers['irc.arcti.ca'] = ['#snifit']
else:
	servers['irc.rizon.io'] = ['#flantest']