import os, imp, random, socket
import settings
from itertools import permutations
from pyxdameraulevenshtein import damerau_levenshtein_distance as distance
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as norm_distance

global ircsocks, ircsock, serverof, cparser
global loaded, perm

# handles exception
def handle_exception(e):
	print(e)

def exec_cmd(modname,inputstr,folder):
	pref = ''
	if folder == settings.folder_mods:
		pref = settings.prefix_mods
	elif folder == settings.folder_events:
		pref = settings.prefix_events
	path = folder+'/'+pref+modname+'.py'
	# print('Loading module from: '+path) # this prints a lot
	mod = imp.load_source(modname,path)
	mod.main(inputstr)

# stuff that should run every iteration of the loop
def run_before(ircmsg):
	ircmsg = ircmsg.strip()
	# runs events
	events = [x.replace('.py','')[len(settings.prefix_events):] for x in os.listdir(settings.folder_events+'/') if x.endswith('.py') and x.startswith(settings.prefix_events)]
	for event in events:
		exec_cmd(event,ircmsg,settings.folder_events)

# stuff to run after cmd parsing
def run_after(ircmsg):
	global loaded
	if not loaded:
		global perm
		reload(settings)

		# calculate permutations of each command
		cmds = cmds_all()
		perm = {}
		for cmd in cmds:
			perm[cmd] = [''.join(p) for p in permutations(cmd)]

		loaded = True

	# quit from removed servers
	if ircsock not in ircsocks:
		quit()

# handles commands of various sorts
def irccommand(cmd, cmdtext, sock=None):
	if sock != None:
		ircsock = sock

	all_commands = cmds_all()
	normal_commands = cmds_normal()

	# don't want random people spamming stuff
	if cmd in settings.cmds_secure:
		if not auth():
			reply_safe(settings.msg_notauth)
			return

	# easy check for disabled commands
	if cmd in settings.cmds_disabled:
		reply_safe(settings.msg_disabled)
		return

	# checks for empty command
	if cmd.strip() == '':
		return

	# execute the command
	cmd = cmd.lower().strip()
	cmdtext = cmdtext.strip()
	if cmd in normal_commands:
		exec_cmd(cmd,cmdtext,settings.folder_mods)

	# attempts to account for typos using Damerau-Levenshtein distance
	else:
		valid = []

		# checks if a valid command is a substring of input
		for cmd_other in all_commands:
			if cmd_other in cmd:
				valid.append(cmd_other)
		# if one is found, then check if input begins with cmd
		# if so, user probably did an accidental concatenation
		if len(valid) == 1:
			if cmd.startswith(valid[0]):
				cmdtext = cmd[len(valid[0]):]+' '+cmdtext

		# checks if D-L distance is 1
		if len(valid) == 0:
			for cmd_other in all_commands:
				if distance(cmd,cmd_other) == 1:
					valid.append(cmd_other)

		# checks if D-L distance is 2 or norm. D-L distance <= 3
		if len(valid) == 0:
			for cmd_other in all_commands:
				if distance(cmd,cmd_other) == 2 or norm_distance(cmd,cmd_other) <= 0.3:
					valid.append(cmd_other)

		# checks if a permutation of a valid command is a substring of input
		if len(valid) == 0:
			for cmd_other in all_commands:
				for p in perm[cmd_other]:
					if p in cmd and cmd_other not in valid:
						valid.append(cmd_other)

		# checks if a unique valid command starts with the input
		if len(valid) == 0:
			for cmd_other in all_commands:
				if cmd_other.startswith(cmd):
					valid.append(cmd_other)

		# check if commands starts with substrings of input
		# probably should be a last resort measure
		substr_len = 1
		while len(valid) == 0 and substr_len <= len(cmd):
			substr_cmd = cmd[:substr_len]
			for cmd_other in all_commands:
				if cmd_other.startswith(substr_cmd):
					valid.append(cmd_other)
			substr_len += 1

		# checks if D-L distance is 3
		if len(valid) == 0:
			for cmd_other in all_commands:
				if distance(cmd,cmd_other) == 3:
					valid.append(cmd_other)

		# checks if there is a permutation with D-L distance of 1
		if len(valid) == 0:
			for cmd_other in all_commands:
				for p in perm[cmd_other]:
					if distance(p,cmd) == 1 and cmd_other not in valid:
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
			if valid[0] in normal_commands:
				irccommand(valid[0], cmdtext)
			else:
				sendmsg(settings.botnick,settings.prefix+valid[0]+' '+cmdtext)
			return
		# reply_safe('Invalid command.') # no need to spam invalid cmd message
		return

# returns a list of dynamically called modules
def cmds_normal():
	return [x.replace('.py','')[len(settings.prefix_mods):] for x in os.listdir(settings.folder_mods+'/') if x.endswith('.py') and x.startswith(settings.prefix_mods)]

# returns a list of undynamic commands
def cmds_special():
	return ['reload']

# returns a list of all mods
def cmds_all():
	return sorted(list(set(cmds_normal()) | set(cmds_special())))

#########################
# IRC NETWORK FUNCTIONS #
#########################

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
	return False
	return current_nick() == 'Kironide'

def ping(msg='pingis'):
	response = 'PONG :'+msg+'\n'
	ircsock.send(response)

def raw(msg):
	ircsock.send(msg+'\n')
def sendmsg(chan, msg):
	ircsock.send('PRIVMSG '+chan+' :'+str(msg)+'\n')
def sendnotice(chan, msg):
	ircsock.send('NOTICE '+chan+' :'+str(msg)+'\n')
def joinchan(chan):
	ircsock.send('JOIN '+chan+'\n')
def partchan(chan):
	ircsock.send('PART '+chan+'\n')
def quit():
	ircsock.send('QUIT :'+settings.msg_quit+'\n')

def reply(msg):
	if cparser.target_is_channel():
		sendmsg(cparser.target, msg)
	else:
		utarget = current_nick()
		sendmsg(utarget, msg)

def reply_safe(msg):
	if msg[-1] == '.':
		msg = msg[:len(msg)-1]
	msg = msg + randext()
	reply(msg)

def notice_current(msg):
	sendmsg(current_nick(),msg)

def current_nick():
	return cparser.nick
def current_user():
	return cparser.user
def current_host():
	return cparser.host
def current_mask():
	return cparser.mask
def current_target():
	return cparser.target