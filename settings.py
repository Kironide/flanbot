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

reload_msg = 'Reloaded utility modules.'

servers = {}
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy']
	servers['irc.rizon.io'] = ['#flantest','#neritic-net','#suikatest']
	servers['irc.arcti.ca'] = ['#snifit']
else:
	servers['irc.rizon.io'] = ['#flantest']