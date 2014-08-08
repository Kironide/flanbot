botnick = 'flanfly'
realname = 'Flandre Scarlet'
prefix = '~'
logfile = 'flanlog.log'
TEST = False

cmds_secure = ['part','msg','raw','server','quit','test']
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
msg_quit = 'Quitting.'

servers = {}
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy','#board2']
	servers['irc.rizon.io'] = ['#flantest','#neritic-net','#suikatest','#/jp/ma','#solidus']
	servers['irc.arcti.ca'] = ['#snifit']
else:
	servers['irc.rizon.io'] = ['#flantest']

seen_buffer = 3