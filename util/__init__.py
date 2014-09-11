import os, imp
import settings
import misc, timeutils, network

global ircsocks, ircsock, serverof, cparser, rtime, psent, precv

# initializes the bot, setting default values and connecting to default servers
def init():
	global ircsocks, serverof, rtime, psent, precv
	ircsocks = []
	serverof = {}
	rtime = {}
	psent = {}
	precv = {}
	for server,channels in settings.servers.items():
		misc.exec_cmd(settings.cmd_server,server,settings.folder_mods)

def handle_msg(ircmsg):
	if ' ' in ircmsg and ircmsg.split(' ')[1] != 'PONG':
		print(ircmsg)

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
def current_sock():
	return ircsock
def current_server():
	return serverof[ircsock]

def inc_psent():
	psent[ircsock] += 1
	psent[ircsock] = psent[ircsock] % settings.ping_modulus
def inc_precv():
	precv[ircsock] += 1
	precv[ircsock] = precv[ircsock] % settings.ping_modulus

def raw(msg):
	ircsock.send(msg+'\n')
def pong(msg):
	ircsock.send('PONG :'+msg+'\n')
def sendmsg(chan, msg):
	ircsock.send('PRIVMSG '+chan+' :'+str(msg)+'\n')
def sendnotice(chan, msg):
	ircsock.send('NOTICE '+chan+' :'+str(msg)+'\n')
def joinchan(chan):
	ircsock.send('JOIN '+chan+'\n')
def partchan(chan):
	ircsock.send('PART '+chan+'\n')
def quit_server():
	ircsocks.remove(ircsock)
def quit():
	ircsock.send('QUIT :'+settings.msg_quit+'\n')
def change_nick(nick):
	ircsock.send('NICK '+nick+'\n')
def ping_server():
	ircsock.send('PING '+current_server()+'\n')
def connect(serv):
	ircsock = network.get_socket(serv)
	ircsocks.append(ircsock)
	serverof[ircsock] = serv
	rtime[ircsock] = timeutils.now()
	psent[ircsock] = 0
	precv[ircsock] = 0

def nickserv_identify(pw, service='NickServ'):
	sendmsg(service,'identify '+pw)
def nickserv_ghost(pw, service='NickServ'):
	sendmsg(service,'ghost '+pw)

def reply(msg):
	if cparser.target_is_channel():
		sendmsg(cparser.target, msg)
	else:
		sendmsg(current_nick(), msg)
def reply_safe(msg):
	if msg[-1] == '.':
		msg = msg[:len(msg)-1]
	reply(msg + misc.randext())
def notice_current(msg):
	sendnotice(current_nick(),msg)

# check if authorized
def auth():
	#return False #kaeru please do not abuse the bot while i sleep :^)
	return current_nick() == 'Kironide'

# stuff that keeps repeating
def run_repeat():
	if timeutils.now() - rtime[ircsock] >= settings.repeat_interval:
		rtime[ircsock] = timeutils.now()
		for repeat in misc.repeats_all():
			misc.exec_cmd(repeat,None,settings.folder_repeat)

		# checks for timeout
		ping_diff = psent[ircsock] - precv[ircsock]
		if ping_diff > settings.ping_timeout_limit:
			print('Timeout detected!')
			quit_server()
			connect(serverof[ircsock])

		# sends regular ping to server
		ping_server()
		inc_psent()

# stuff that should run every iteration of the loop
def run_before(ircmsg):
	# runs events
	for event in misc.events_all():
		misc.exec_cmd(event,ircmsg.strip(),settings.folder_events)

	# checks for pong response to our pings
	if ' ' in ircmsg and ircmsg.split(' ')[1] == 'PONG':
		inc_precv()

# stuff to run after cmd parsing
def run_after(ircmsg):
	# quit from removed servers
	if ircsock not in ircsocks:
		quit()

# handles commands of various sorts
def irccommand(cmd, cmdtext):
	cmd = cmd.lower().strip()
	cmdtext = cmdtext.strip()

	# checks for empty command
	if cmd.strip() == '':
		return

	# don't want random people spamming stuff
	if cmd in settings.cmds_secure and not auth():
		reply_safe(settings.msg_notauth)
		return

	# easy check for disabled commands
	if cmd in settings.cmds_disabled:
		reply_safe(settings.msg_disabled)
		return

	# execute the command
	if cmd in misc.cmds_normal():
		misc.exec_cmd(cmd,cmdtext,settings.folder_mods)

	# attempts to account for typos
	else:
		match = misc.match_input(cmd,misc.cmds_all())
		if match != None:
			correct = match[0]
			cmdtext = match[1]+' '+cmdtext
			reply_safe('I\'ll interpret that command as \''+correct+'\'. Maybe you made a typo.')
			if correct != 'reload':
				irccommand(correct, cmdtext)
			else:
				sendmsg(settings.botnick,settings.prefix+correct+' '+cmdtext)
			return
		# reply_safe('Invalid command.') # no need to spam invalid cmd message
		return