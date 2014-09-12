#!/usr/bin/env python
import util.parser, util.misc, util.timeutils, util.network
import settings

class FlanBot:
	def __init__(self):
		self.ircsocks = []
		self.serverof = {}
		self.rtime = {}
		self.psent = {}
		self.precv = {}
		self.cparser = None
		self.ircsock = None
		for server in settings.servers:
			self.connect_server(server)

	def handle_msg(self, ircmsg):
		if ' ' in ircmsg and ircmsg.split(' ')[1] != 'PONG':
			print(ircmsg)

	def current_nick(self):
		return self.cparser.nick
	def current_user(self):
		return self.cparser.user
	def current_host(self):
		return self.cparser.host
	def current_mask(self):
		return self.cparser.mask
	def current_target(self):
		return self.cparser.target
	def current_sock(self):
		return self.ircsock
	def current_server(self):
		return self.serverof[self.ircsock]

	def inc_psent(self):
		self.psent[self.ircsock] += 1
		self.psent[self.ircsock] = self.psent[self.ircsock] % settings.ping_modulus
	def inc_precv(self):
		self.precv[self.ircsock] += 1
		self.precv[self.ircsock] = self.precv[self.ircsock] % settings.ping_modulus

	def send(self, msg):
		self.ircsock.send(msg+'\n')
	def ping(self):
		self.send('PING '+self.current_server()+'\n')
	def pong(self, msg):
		self.send('PONG :'+msg+'\n')
	def send_msg(self, chan, msg):
		self.send('PRIVMSG '+chan+' :'+str(msg)+'\n')
	def send_notice(self, chan, msg):
		self.send('NOTICE '+chan+' :'+str(msg)+'\n')
	def join(self, chan):
		self.send('JOIN '+chan+'\n')
	def part(self, chan):
		self.send('PART '+chan+'\n')
	def quit(self):
		self.send('QUIT :'+settings.msg_quit+'\n')
	def change_nick(self, nick):
		self.send('NICK '+nick+'\n')

	def connect_server(self, server):
		ircsock = util.network.get_socket(server)
		self.ircsocks.append(ircsock)
		self.serverof[ircsock] = server
		self.rtime[ircsock] = util.timeutils.now()
		self.psent[ircsock] = 0
		self.precv[ircsock] = 0
	def quit_server(self):
		self.ircsocks.remove(ircsock)

	def nickserv_identify(self, pw):
		self.send_msg('NickServ','identify '+pw)
	def nickserv_ghost(self, pw):
		self.send_msg('NickServ','ghost '+pw)

	def reply(self, msg):
		if self.cparser.target_is_channel():
			self.send_msg(self.cparser.target, msg)
		else:
			self.send_msg(self.current_nick(), msg)
	def reply_safe(self, msg):
		if msg[-1] == '.':
			msg = msg[:len(msg)-1]
		self.reply(msg + util.misc.randext())
	def reply_notice(self, msg):
		self.send_notice(self.current_nick(),msg)

	def auth(self):
		return self.current_nick() == 'Kironide'

	def run_repeat(self):
		if util.timeutils.now() - self.rtime[self.ircsock] >= settings.repeat_interval:
			self.rtime[self.ircsock] = util.timeutils.now()
			for repeat in util.misc.repeats_all():
				self.exec_cmd(repeat,None,settings.folder_repeat)

			# checks for timeout
			ping_diff = self.psent[self.ircsock] - self.precv[self.ircsock]
			if ping_diff > settings.ping_timeout_limit:
				print('Timeout detected!')
				self.quit_server()
				self.connect_server(self.serverof[self.ircsock])

			# sends regular ping to server
			self.ping()
			self.inc_psent()

	def run_before(self, ircmsg):
		for event in util.misc.events_all():
			self.exec_cmd(event,ircmsg.strip(),settings.folder_events)

		# checks for pong response to our pings
		if ' ' in ircmsg and ircmsg.split(' ')[1] == 'PONG':
			self.inc_precv()

	def run_after(self, ircmsg):
		if self.ircsock not in self.ircsocks:
			self.quit()

	def irccommand(self, cmd, cmdtext):
		cmd = cmd.lower().strip()
		cmdtext = cmdtext.strip()

		# checks for empty command
		if cmd.strip() == '':
			return

		# don't want random people spamming stuff
		if cmd in settings.cmds_secure and not self.auth():
			self.reply_safe(settings.msg_notauth)
			return

		# easy check for disabled commands
		if cmd in settings.cmds_disabled:
			self.reply_safe(settings.msg_disabled)
			return

		# execute the command
		if cmd in util.misc.cmds_normal():
			self.exec_cmd(cmd,cmdtext,settings.folder_mods)

		# attempts to account for typos
		else:
			match = util.misc.match_input(cmd,misc.cmds_all())
			if match != None:
				correct = match[0]
				cmdtext = match[1]+' '+cmdtext
				self.reply_safe('I\'ll interpret that command as \''+correct+'\'. Maybe you made a typo.')
				if correct != 'reload':
					self.irccommand(correct, cmdtext)
				else:
					self.send_msg(settings.botnick,settings.prefix+correct+' '+cmdtext)
				return
			return

	# execute command
	def exec_cmd(self, modname, inputstr, folder):
		import imp, multiprocessing
		pref = ''
		if folder == settings.folder_mods:
			pref = settings.prefix_mods
		elif folder == settings.folder_events:
			pref = settings.prefix_events
		elif folder == settings.folder_repeat:
			pref = settings.prefix_repeat
		path = folder+'/'+pref+modname+'.py'
		# print('Loading module from: '+path) # this prints a lot
		mod = imp.load_source(modname,path)
		if modname in ['server','quit']:
			mod.main(inputstr)
		else:
			if inputstr == None:
				p = multiprocessing.Process(target=mod.main,args=(self,))
			else:
				p = multiprocessing.Process(target=mod.main,args=(self,inputstr,))
			p.start()
			p.join()
