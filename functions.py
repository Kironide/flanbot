import re
import util
global ircsock, user, dtype, target

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
			reply(msg)
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
				later_msg = ' '.join(temp[1:])
				util.add_later(later_nick, util.get_nick(user), later_msg)
				reply('Message to '+later_nick+' recorded.')
	else:
		reply('Invalid command.')
