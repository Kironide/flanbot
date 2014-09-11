botnick = 'flanfly'
nick_ext = '_'
realname = 'Flandre Scarlet'
prefix = '~'
logfile = 'flanlog.log'
repeat_interval = 1
mod_server = 'server'
TEST = False
time_parse_truncate = 3

cmds_secure = ['part','msg','raw','server','quit','test']
cmds_disabled = []

datafile_later = 'data/later.dat'
datafile_seen = 'data/seen.dat'
datafile_chaninfo = 'data/chaninfo.dat'
datafile_mafia = 'data/mafia.dat'
datafile_remind = 'data/remind.dat'

prefix_mods = 'mod_'
folder_mods = 'mods'

prefix_events = 'event_'
folder_events = 'events'

folder_books = 'books'

prefix_repeat = 'repeat_'
folder_repeat = 'repeat'

msg_reload = 'Reloaded utility modules.'
msg_notauth = 'You are not authorized for this command.'
msg_disabled = 'That command is turned off.'
msg_nobook = 'I don\'t have that book on hand.'
msg_quit = 'Quitting.'

servers = {}
if not TEST:
	servers['nucleus.kafuka.org'] = ['#fraxy','#board2']
	servers['irc.rizon.net'] = ['#flantest','#neritic-net','#suikatest','#/jp/ma','#solidus','#quizup','#elona','#batoru']
	servers['irc.efnet.net'] = ['#snifit']
else:
	servers['irc.rizon.net'] = ['#flantest']
	servers['nucleus.kafuka.org'] = ['#flantest']

server_alias = {
	'irc.rizon.net': 'irc.rizon.io'
	,'irc.efnet.net': 'irc.arcti.ca'
}

seen_buffer = 3
recv_data_amount = 2048

responses = [
'.'
,'!'
,'. Remember, bullying is bad!'
,'. Bullies will be the first against the wall!'
,'. Transform: Anti-Bully Ranger!'
,'. Are you living the NEET life yet?'
,'. Are you living the literary life yet?'
,'... Hello? Please respond!'
,'. It can\'t be helped...'
,'. n-not like I wanted to or anything, b-baka!'
,'. The best time of the day is flanally here!'
,'. For you.'
,'. Sasuga onii-sama!'
,', onii-chan!'
]