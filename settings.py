botnick = 'flanfly'
nick_ext = '_'
realname = 'Flandre Scarlet'
prefix = '~'
logfile = 'flanlog.log'
TEST = False

cmds_secure = ['part','msg','raw','server','quit','test']
cmds_disabled = []

datafile_later = 'data/later.dat'
datafile_seen = 'data/seen.dat'
datafile_chaninfo = 'data/chaninfo.dat'

prefix_mods = 'mod_'
folder_mods = 'mods'

prefix_events = 'event_'
folder_events = 'events'

folder_books = 'books'

msg_reload = 'Reloaded utility modules.'
msg_notauth = 'You are not authorized for this command.'
msg_disabled = 'That command is turned off.'
msg_quit = 'Quitting.'

servers = {}
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy','#board2']
	servers['irc.rizon.io'] = ['#flantest','#neritic-net','#suikatest','#/jp/ma','#solidus','#quizup','#elona','#batoru']
	servers['irc.arcti.ca'] = ['#snifit']
else:
	servers['irc.rizon.io'] = ['#flantest']
	servers['nucleus.kafuka.org'] = ['#flantest']

seen_buffer = 3
recv_data_amount = 2048

responses = [
'.',
'!',
'. Remember, bullying is bad!',
'. Bullies will be the first against the wall!',
'. Did you know Plato was the first anti-bully?',
'. Transform: Anti-Bully Ranger!',
'. Are you living the NEET life yet?',
'. Are you living the literary life yet?',
'... Hello? Please respond!',
'. It can\'t be helped...',
'. n-not like I wanted to or anything, b-baka!',
'. The best time of the day is flanally here!',
'. I would do anything for you!',
', but can Shiki kill Servants?',
'! Believe in me who believes in you!',
'. For you.',
'! Super interesting!',
'. Sasuga onii-sama!'
]