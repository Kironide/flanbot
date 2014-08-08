botnick = 'flanfly'
realname = 'Flandre Scarlet'
prefix = '~'
logfile = 'flanlog.log'
TEST = True

cmds_secure = ['part','msg','raw']
cmds_disabled = []

datafile_later = 'data/later.dat'
datafile_seen = 'data/seen.dat'

prefix_mods = 'mod_'
folder_mods = 'mods'

prefix_events = 'event_'
folder_events = 'events'

msg_reload = 'Reloaded utility modules.'
msg_notauth = 'You are not authorized for this command.'
msg_disabled = 'That command is turned off.'

servers = {}
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy']
	servers['irc.rizon.io'] = ['#flantest','#neritic-net','#suikatest','#/jp/ma']
	servers['irc.arcti.ca'] = ['#snifit']
else:
	servers['irc.rizon.io'] = ['#flantest']

seen_buffer = 3