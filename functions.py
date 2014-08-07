import re, random, requests, json, HTMLParser
import init, util
from BeautifulSoup import BeautifulSoup as bs4
from pyxdameraulevenshtein import damerau_levenshtein_distance as distance
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as norm_distance
global ircsock, serverof, user, dtype, target, later, loaded

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
	'. Hello, please respond...',
	', you piece of shit.'
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
def irccommand(cmd, cmdtext):
	cmds_normal = ['help','join','part','msg','rthread','later','msg']
	cmds_special = ['reload','server','quit']
	cmds_all = list(set(cmds_normal) | set(cmds_special))
	auth_needed = ['part','msg']
	disabled = []

	# don't want random people spamming stuff
	if cmd in auth_needed:
		if not auth():
			reply_safe('You are not authorized for that command.')
			return

	# easy check for disabled commands
	if cmd in disabled:
		reply_safe('That command is turned off.')
		return

	cmd = cmd.lower()
	if cmd == 'help':
		reply_safe('Currently available commands are: help, reload, join, part, later, rthread.')
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
		for cmd_other in cmds_all:
			if distance(cmd,cmd_other) == 1:
				valid.append(cmd_other)
		if len(valid) == 0:
			for cmd_other in cmds_all:
				if distance(cmd,cmd_other) == 2 or norm_distance(cmd,cmd_other) <= 0.3:
					valid.append(cmd_other)
		if len(valid) > 1:
			to_remove = []
			for cmd_temp in valid:
				if cmd_temp[0] != cmd[0]:
					to_remove.append(cmd_temp)
			for cmd_temp in to_remove:
				valid.remove(cmd_temp)
		if len(valid) == 1:
			if valid[0] in cmds_normal:
				irccommand(valid[0], cmdtext)
			else:
				sendmsg(init.botnick,init.prefix+valid[0]+' '+cmdtext)
			return
		reply_safe('Invalid command.')

# stuff that should run every iteration of the loop
def run_every_time(msg):
	global later, loaded

	# check for existence of later info
	if not loaded:
		later = util.get_later()
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