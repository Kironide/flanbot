import re, random
import util
global ircsock, user, dtype, target
global later_conf

def randext():
	r = random.randint(1,12)
	if r == 1:
		return '.'
	elif r == 2:
		return '...'
	elif r == 3:
		return '!'
	elif r == 4:
		return ', probably.'
	elif r == 5:
		return ', I think.'
	elif r == 6:
		return '. Remember, bullying is bad!'
	elif r == 7:
		return '. Bullies will be the first against the wall!'
	elif r == 8:
		return ', more or less.'
	elif r == 9:
		return '. Did you know Plato was the first anti-bully?'
	elif r == 10:
		return '. Transform: Anti-Bully Ranger!'
	elif r == 10:
		return '. Are you living the NEET life yet?'
	elif r == 11:
		return '. Are you living the literary life yet?'
	elif r == 12:
		return '. Hello, please respond...'

def ping():
	ircsock.send('PONG :pingis\n')

def reply(msg):
	if target[0] == '#':
		sendmsg(target, msg)
	else:
		utarget = util.get_nick(user)
		sendmsg(utarget, msg)

def sendmsg(chan, msg):
	ircsock.send('PRIVMSG '+chan+' :'+str(msg)+'\n')

def joinchan(chan):
	ircsock.send('JOIN '+chan+'\n')

def partchan(chan):
	ircsock.send('PART '+chan+'\n')

# checks for msgs
def check_later(nick, later):
	if util.in_later(nick,later):
		print('found')
		messages = util.read_later(nick)
		for msg in messages:
			reply(msg+' '*random.randint(1,9))
		util.remove_later(nick)
		return True
	return False

def irccommand(cmd, cmdtext):
	if cmd == 'help':
		reply('Currently available commands are: help, reload, join, part, later')
	elif cmd == 'join':
		joinchan(cmdtext.split(' ')[0])
	elif cmd == 'part':
		partchan(cmdtext.split(' ')[0])
	elif cmd == 'later':
		if cmdtext[:5] == 'tell ':
			if len(cmdtext.split(' ')) < 3:
				reply('Command has too few arguments.')
			else:
				irccommand(cmd, cmdtext[5:])
		else:
			if len(cmdtext.split(' ')) < 2:
				reply('Command has too few arguments.')
			else:
				temp = cmdtext.split(' ')
				later_nick = temp[0]
				if len(later_nick) >= 3 and later_nick[:3].lower() == 'xpc':
					reply('You know he doesn\'t like that'+randext())
				else:
					later_msg = ' '.join(temp[1:])
					add = util.add_later(later_nick, util.get_nick(user), later_msg)
					if add:
						reply('Message to '+later_nick+' recorded'+randext())
					else:
						reply('You\'ve already sent that message three times already'+randext())
	else:
		reply('Invalid command.')
