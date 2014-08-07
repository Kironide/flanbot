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

import sys
import init, util
from itertools import permutations
from pyxdameraulevenshtein import damerau_levenshtein_distance as distance
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as norm_distance

global later, loaded, perm

def execute_command(cmd,cmdtext):
	path = sys.path
	sys.path.append('flanmods/')
	mod = __import__(cmd)
	reload(mod)
	mod.main(cmdtext)
	sys.path = path

	if cmd == 'later':
		global later
		later = util.get_later()

# handles commands of various sorts
def irccommand(cmd, cmdtext, get_commands=False):
	ircsock = util.ircsock

	cmds_secure = ['part','msg']
	cmds_disabled = []

	cmds_all = util.cmds_all()
	cmds_normal = util.cmds_normal()

	# returns list of commands
	if get_commands:
		return cmds_all

	# don't want random people spamming stuff
	if cmd in cmds_secure:
		if not util.auth():
			util.reply_safe('You are not authorized for that command.')
			return

	# easy check for disabled commands
	if cmd in cmds_disabled:
		util.reply_safe('That command is turned off.')
		return

	cmd = cmd.lower()
	cmdtext = cmdtext.strip()

	if cmd in cmds_normal:
		execute_command(cmd,cmdtext)
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
			util.reply_safe('I\'ll interpret that command as \''+valid[0]+'\'. Maybe you made a typo.')
			if valid[0] in cmds_normal:
				irccommand(valid[0], cmdtext)
			else:
				util.sendmsg(init.botnick,init.prefix+valid[0]+' '+cmdtext)
			return
		util.reply_safe('Invalid command.')

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
			util.user = msg[0][1:]
			util.dtype = msg[1]
			util.target = msg[2]
			nick = util.current_nick()

			global later
			found = util.later_check(nick, later)
			if found:
				later = util.get_later()

		# records messages/quits/parts/joins for seen command data
		elif event == 'seen':
			util.user = msg[0][1:]
			util.dtype = msg[1]
			util.target = msg[2]
			text = ' '.join(msg[3:])[1:]
			util.seen_record(text)
	except Exception, e:
		print(e)