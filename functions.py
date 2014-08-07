"""
To-do list:
- improve code structure
- try to get more stuff out of flanbot.py and into functions.py/util.py
- socket connect server thing, get efnet to work
- add url/yt info feature
- maybe add smart server selection like ~server rizon connects to irc.rizon.net
- move the html parsing methods to util
- think about vowel-removal combinations for typo correction
- figure out how to make plugins/ folder
	- move ircsock-requiring methods to util
	- move randext to util as well
	- use http://stackoverflow.com/questions/13598035/importing-a-module-when-the-module-name-is-in-a-variable to figure this out
	- 
"""

import re, random, requests, json, HTMLParser
import init, util
from itertools import permutations
from BeautifulSoup import BeautifulSoup as bs4
from pyxdameraulevenshtein import damerau_levenshtein_distance as distance
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as norm_distance

global ircsock, serverof, user, dtype, target, later, loaded, perm

# a random thing to append to the end of messages
def randext():
	responses = [
	'.',
	'...',
	'!',
	', probably.',
	', I think.',
	', I think.',
	'. Remember, bullying is bad!',
	'. Bullies will be the first against the wall!',
	', more or less.',
	'. Did you know Plato was the first anti-bully?',
	'. Transform: Anti-Bully Ranger!',
	'. Are you living the NEET life yet?',
	'. Are you living the literary life yet?',
	'... Hello? Please respond!',
	', you piece of shit.',
	'. It can\'t be helped...'
	]
	return responses[random.randint(1,len(responses))-1]

# check if authorized
def auth():
	return util.get_nick(user) == 'Kironide'

# strip tags from HTML content
def strip_tags(html):
	return ''.join(bs4(html).findAll(text=True))

# formats html entitites
def format_html_entities(html):
	h = HTMLParser.HTMLParser()
	return h.unescape(html)

def ping():
	ircsock.send('PONG :pingis\n')

def reply(msg):
	if target[0] == '#':
		sendmsg(target, msg)
	else:
		utarget = util.get_nick(user)
		sendmsg(utarget, msg)

def reply_safe(msg):
	if msg[-1] == '.':
		msg = msg[:len(msg)-1]
	msg = msg + randext()
	reply(msg)

def sendmsg(chan, msg):
	ircsock.send('PRIVMSG '+chan+' :'+str(msg)+'\n')

def joinchan(chan):
	ircsock.send('JOIN '+chan+'\n')

def partchan(chan):
	ircsock.send('PART '+chan+'\n')

def quit(msg='Quitting.'):
	reply_safe('This function is not implemented yet.')
	#ircsock.send('QUIT '+msg+'\n')

# checks for msgs
def check_later(nick):
	global later
	if util.in_later(nick,later):
		messages = util.read_later(nick)
		for msg in messages:
			reply(msg)
		util.remove_later(nick)
		return True
	return False

# records seen data
def record_seen(text):
	asdf = True

# handles commands of various sorts
def irccommand(cmd, cmdtext, get_commands=False):
	cmds_normal = ['help','join','part','msg','rthread','later','msg']
	cmds_special = ['reload','server','quit']
	cmds_secure = ['part','msg']
	cmds_disabled = []

	cmds_all = list(set(cmds_normal) | set(cmds_special))

	# returns list of commands
	if get_commands:
		return cmds_all

	# don't want random people spamming stuff
	if cmd in cmds_secure:
		if not auth():
			reply_safe('You are not authorized for that command.')
			return

	# easy check for disabled commands
	if cmd in cmds_disabled:
		reply_safe('That command is turned off.')
		return

	cmd = cmd.lower()
	cmdtext = cmdtext.strip()

	if cmd == 'help':
		if cmdtext == '':
			reply_safe('Currently available commands are: '+', '.join(cmds_all)+'. Type '+init.prefix+'help [command] for a detailed description.')
		else:
			help_text = {
			'help': 'Syntax: help [optional: command]. Displays help.',
			'reload': 'Syntax: reload. Reloads bot functions.',
			'server': 'Syntax: server [address]. Connects to the specified server.',
			'quit': 'Syntax: quit [optional: message]. Disconnects from the current server.',
			'join': 'Syntax: join [channel]. Joins the specified channel.',
			'part': 'Syntax: part [channel]. Parts the specified channel.',
			'later': 'Syntax: later [optional: tell] [nick] [message]. Leaves a message for [nick] when they join or say something.',
			'rthread': 'Syntax: rthread [optional: board]. Gets a random thread from a specified 4chan board or from a random board if unspecified.'
			}
			for cmd_temp,value in help_text.items():
				help_text[cmd_temp] = help_text[cmd_temp].replace('Syntax: ','Syntax: '+init.prefix)
			help_cmd = cmdtext.split(' ')[0]
			if help_cmd in help_text:
				reply_safe(help_text[help_cmd])
			elif help_cmd not in cmds_all:
				reply_safe('That command does not exist.')
			else:
				reply_safe('Sorry, no help text has been set for that command yet.')
	elif cmd == 'join':
		if cmdtext.split(' ')[0].lower() == '#dontjoinitsatrap':
			reply_safe('Nice try, nerd.')
		else:
			joinchan(cmdtext.split(' ')[0])
	elif cmd == 'part':
		partchan(cmdtext.split(' ')[0])
	elif cmd == 'msg':
		recipient = cmdtext.split(' ')[0]
		message = ' '.join(cmdtext.split(' ')[1:])
		sendmsg(recipient, message)
	elif cmd == 'rthread':
		s = requests.Session()
		if cmdtext == '':
			boards = json.loads(s.get('http://a.4cdn.org/boards.json').text)['boards']
			rboard = boards[random.randint(1,len(boards))-1]['board']
			irccommand(cmd, rboard)
		else:
			try:
				cat = json.loads(s.get('http://a.4cdn.org/'+cmdtext.split(' ')[0]+'/catalog.json').text)
				threads = []
				for page in cat:
					for thread in page['threads']:
						threads.append(thread)
				rthread = threads[random.randint(1,len(threads))-1]
				if 'sub' in rthread:
					subj = rthread['sub'].encode('utf-8')
				else:
					subj = 'None'
				post = format_html_entities(strip_tags(rthread['com'].replace('<br>',' '))).encode('utf-8')
				if len(post) > 150:
					post = post[:150] + '...'
				reply('http://boards.4chan.org/'+cmdtext+'/thread/'+str(rthread['no'])+' Subject: '+subj+', Post: '+post)
			except Exception, e:
				reply_safe('Invalid board selection.')
				print(e)
	elif cmd == 'later':
		if cmdtext[:5] == 'tell ':
			if len(cmdtext.split(' ')) < 3:
				reply_safe('Command has too few arguments.')
			else:
				irccommand(cmd, cmdtext[5:])
		else:
			if len(cmdtext.split(' ')) < 2:
				reply_safe('Command has too few arguments.')
			else:
				temp = cmdtext.split(' ')
				later_nick = temp[0]
				if len(later_nick) >= 3 and later_nick[:3].lower() == 'xpc':
					reply_safe('You know he doesn\'t like that.')
				else:
					later_msg = ' '.join(temp[1:])
					add = util.add_later(later_nick, util.get_nick(user), later_msg)
					if add:
						reply_safe('Message to '+later_nick+' recorded.')
						global later
						later = util.get_later()
					else:
						reply_safe('You\'ve already sent that message three times already.')
	else:
		# attempts to account for typos using Damerau-Levenshtein distance
		valid = []

		# checks if a valid command is a substring of input
		for cmd_other in cmds_all:
			if cmd_other in cmd:
				valid.append(cmd_other)
		# if one is found, then check if input begins with cmd
		# if so, user probably did an accidental concatenation
		if len(valid) == 1:
			if cmd.startswith(valid[0]):
				cmdtext = cmd[len(valid[0]):]+' '+cmdtext

		# checks if D-L distance is 1
		if len(valid) == 0:
			for cmd_other in cmds_all:
				if distance(cmd,cmd_other) == 1:
					valid.append(cmd_other)

		# checks if D-L distance is 2 or norm. D-L distance <= 3
		if len(valid) == 0:
			for cmd_other in cmds_all:
				if distance(cmd,cmd_other) == 2 or norm_distance(cmd,cmd_other) <= 0.3:
					valid.append(cmd_other)

		# checks if a permutation of a valid command is a substring of input
		if len(valid) == 0:
			global perm
			for cmd_other in cmds_all:
				for p in perm[cmd_other]:
					if p in cmd and cmd_other not in valid:
						valid.append(cmd_other)

		# checks if a unique valid command starts with the input
		if len(valid) == 0:
			for cmd_other in cmds_all:
				if cmd_other.startswith(cmd):
					valid.append(cmd_other)

		# if there are multiple valid commands found, choose the one that starts
		# with same letter as input (if unique)
		if len(valid) > 1:
			to_remove = []
			for cmd_temp in valid:
				if cmd_temp[0] != cmd[0]:
					to_remove.append(cmd_temp)
			for cmd_temp in to_remove:
				valid.remove(cmd_temp)

		# if unique match found, then use that command
		if len(valid) == 1:
			reply_safe('I\'ll interpret that command as \''+valid[0]+'\'. Maybe you made a typo.')
			if valid[0] in cmds_normal:
				irccommand(valid[0], cmdtext)
			else:
				sendmsg(init.botnick,init.prefix+valid[0]+' '+cmdtext)
			return
		reply_safe('Invalid command.')

# stuff that should run every iteration of the loop
def run_every_time(msg):
	global loaded

	# load initial data and stuff like that
	if not loaded:
		global later, perm

		# load later.dat
		later = util.get_later()

		# calculate permutations of each command
		cmds = irccommand('','',get_commands=True)
		perm = {}
		for cmd in cmds:
			perm[cmd] = [''.join(p) for p in permutations(cmd)]

		loaded = True


	# checks for validity of various conditions given an irc event
	conditions = {
	'later': len(msg) >= 3 and (msg[1] == 'PRIVMSG' or msg[1] == 'JOIN'),
	'seen': len(msg) >= 3 and msg[1] in ['PRIVMSG','QUIT','PART','JOIN']
	}
	for event,condition in conditions.items():
		if condition:
			event_action(msg, event)

# stuff for the above
def event_action(msg, event):
	try:
		# checks for a later message to send upon PRIVMSG or JOIN
		if event == 'later':
			user = msg[0][1:]
			dtype = msg[1]
			target = msg[2]
			nick = util.get_nick(user)

			found = check_later(nick)
			if found:
				later = util.get_later()

		# records messages/quits/parts/joins for seen command data
		elif event == 'seen':
			user = msg[0][1:]
			dtype = msg[1]
			target = msg[2]
			text = ' '.join(msg[3:])[1:]
			record_seen(text)
	except Exception, e:
		print(e)