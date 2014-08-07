import os, pickle, time, math, random, HTMLParser
from BeautifulSoup import BeautifulSoup as bs4
global ircsock, user, dtype, target, serverof

# returns the formatted time difference between a timestamp and current time
def timediff(ts):
	diff = int(time.time())- int(ts)
	if diff < 60:
		return str(diff)+'s ago'
	minutes = math.floor(diff/60.0)
	seconds = diff - minutes*60
	if minutes < 60:
		return str(int(minutes))+'m'+str(int(seconds))+'s ago'
	hours = math.floor(minutes/60.0)
	minutes = minutes - hours*60
	if hours < 24:
		return str(int(hours))+'h'+str(int(minutes))+'m ago'
	days = math.floor(hours/24.0)
	hours = hours - days*24
	return str(int(days))+'d'+str(int(hours))+'h ago'

# returns a list of dynamically called modules
def cmds_normal():
	return [x.replace('.py','') for x in os.listdir('flanmods/') if x.endswith('py')]

# returns a list of undynamic commands
def cmds_special():
	return ['reload','server','quit']

# returns a list of all mods
def cmds_all():
	return sorted(list(set(cmds_normal()) | set(cmds_special())))

################
# HTML PARSING #
################

# strip tags from HTML content
def strip_tags(html):
	return ''.join(bs4(html).findAll(text=True))

# formats html entitites
def format_html_entities(html):
	h = HTMLParser.HTMLParser()
	return h.unescape(html)

#########################
# IRC NETWORK FUNCTIONS #
#########################

# returns just the nick from stuff!idk@whatever
def get_nick(username):
	return username.split('!')[0].replace(':','')

# returns the "current" nick
def current_nick():
	return get_nick(user)

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
	return current_nick() == 'Kironide'

def ping(msg='pingis'):
	response = 'PONG :'+msg+'\n'
	ircsock.send(response)
	print('Responded to ping request with: '+response.strip())

def sendmsg(chan, msg):
	ircsock.send('PRIVMSG '+chan+' :'+str(msg)+'\n')

def joinchan(chan):
	ircsock.send('JOIN '+chan+'\n')

def partchan(chan):
	ircsock.send('PART '+chan+'\n')

def quit(msg='Quitting.'):
	reply_safe('This function is not implemented yet.')
	#ircsock.send('QUIT '+msg+'\n')

def reply(msg):
	if target[0] == '#':
		sendmsg(target, msg)
	else:
		utarget = current_nick()
		sendmsg(utarget, msg)

def reply_safe(msg):
	if msg[-1] == '.':
		msg = msg[:len(msg)-1]
	msg = msg + randext()
	reply(msg)

def raw(msg):
	ircsock.send(msg+'\n')

######################################
# STUFF RELATED TO THE LATER COMMAND #
######################################

# returns the pickled object in later.dat
# creates file with empty dict if it doesn't exist
# keys are usernames, values are lists of messages
# each message is stored as [timestamp, fromuser, msg]
def get_later():
	if not os.path.exists('later.dat'):
		with open('later.dat','w') as f:
			temp = {}
			pickle.dump(temp,f)
	with open('later.dat','r') as f:
		temp = pickle.load(f)
	return temp

# save the later object to later.dat
def save_later(later):
	with open('later.dat','w') as f:
		pickle.dump(later,f)

# adds a msg to send to the later object
# nick is the person to send to
# user is the person who sent it
def later_add(nick, user, msg):
	times = later_count(nick, user, msg)
	if times >= 3:
		return False
	later = get_later()
	if nick not in later:
		later[nick] = []
	later[nick].append([time.time(), user, msg])
	save_later(later)
	return True

# removes a user from the later object
def later_remove(nick):
	later = get_later()
	to_remove = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			to_remove.append(nick_later)
	for nick_later in to_remove:
		later.pop(nick_later, None)
	save_later(later)

# gets a list of messages to send for a certain nick
def later_read(nick):
	later = get_later()
	rawmsg = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for msg in msgs:
				rawmsg.append(msg)
	to_send = []
	for item in rawmsg:
		##to_send.append(nick+': ['+datetime.datetime.fromtimestamp(int(item[0])).strftime('%Y-%m-%d %H:%M:%S')+']<'+item[1]+'> '+item[2])
		to_send.append(nick+': ('+timediff(item[0])+') <'+item[1]+'> '+item[2])
	return to_send

# returns true if nick is in later
def later_contains(nick, later=None):
	if later == None:
		later = get_later()
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			return True
	return False

# number of times a message is recorded for someone
def later_count(nick, user, msg):
	later = get_later()
	times = 0
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for item in msgs:
				if msg == item[2] and user.lower() == item[1].lower():
					times += 1
	return times

# checks for msgs
def later_check(nick, later):
	if later_contains(nick,later):
		messages = later_read(nick)
		for msg in messages:
			reply(msg)
		later_remove(nick)
		return True
	return False

#####################################
# STUFF RELATED TO THE SEEN COMMAND #
#####################################

# save data about someone
def seen_save(nick, type, msg=''):
	# create data file if it doesn't exist
	if not os.path.exists('seen.dat'):
		with open('seen.dat','w') as f:
			test = 1

# records seen data
def seen_record(text):
	asdf = True