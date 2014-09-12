#!/usr/bin/env python
import util.parser, util.misc, util.timeutils, util.network
import settings

class Connection:
	def __init__(self, server):
		self.server = server
		self.socket = util.network.get_socket(server)
		self.rtime = util.timeutils.now()
		self.psent = 0
		self.precv = 0
	def inc_psent(self):
		self.psent = (self.psent + 1) % settings.ping_modulus
	def inc_precv(self):
		self.precv = (self.precv + 1) % settings.ping_modulus
	def send(self, msg):
		self.socket.send(msg+'\n')

class FlanBot:
	def __init__(self, copy=False):
		if not copy:
			self.connections, self.cparser, self.conn = [], None, None
			for server in settings.servers:
				self.connect_server(server)

	def next_conn(self):
		pos = -1
		if self.conn in self.connections:
			pos = self.connections.index(self.conn)
		pos = (pos + 1) % len(self.connections)
		self.conn = self.connections[pos]

	# prints server message, writes to logfile, and returns parser class instance
	def handle_msg(self, ircmsg):
		if ' ' in ircmsg and ircmsg.split(' ')[1] != 'PONG':
			print(ircmsg)
		with open(settings.logfile,'a') as f:
			f.write(ircmsg+'\n')
		return util.parser.get_parser(ircmsg)

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
	def current_server(self):
		return self.conn.server

	def receive(self):
		try:
			return self.conn.socket.recv(settings.recv_data_amount).strip('\r\n').split('\r\n')
		except:
			return []

	def ping(self):
		self.conn.send('PING '+self.current_server()+'\n')
	def pong(self, msg):
		self.conn.send('PONG :'+msg+'\n')
	def send_msg(self, chan, msg):
		self.conn.send('PRIVMSG '+chan+' :'+str(msg)+'\n')
	def send_notice(self, chan, msg):
		self.conn.send('NOTICE '+chan+' :'+str(msg)+'\n')
	def join(self, chan):
		self.conn.send('JOIN '+chan+'\n')
	def part(self, chan):
		self.conn.send('PART '+chan+'\n')
	def quit(self):
		self.conn.send('QUIT :'+settings.msg_quit+'\n')
	def change_nick(self, nick):
		self.conn.send('NICK '+nick+'\n')

	def connect_server(self, server):
		self.connections.append(Connection(server))
	def quit_server(self):
		self.connections.remove(self.conn)

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
		self.conn.send_notice(self.current_nick(),msg)

	def auth(self):
		return self.current_nick() == 'Kironide'

	def run_repeat(self):
		if util.timeutils.now() - self.conn.rtime >= settings.repeat_interval:
			self.conn.rtime = util.timeutils.now()
			for repeat in util.misc.repeats_all():
				self.exec_cmd(repeat,None,settings.folder_repeat)

			# checks for timeout
			ping_diff = self.conn.psent - self.conn.precv
			if ping_diff > settings.ping_timeout_limit:
				print('Timeout detected!')
				self.quit_server()
				self.connect_server(self.conn.server)

			# sends regular ping to server
			self.ping()
			self.conn.inc_psent()

	def run_actions(self, ircmsg, parser):
		# executes events in the events folder
		for event in util.misc.events_all():
			self.exec_cmd(event,ircmsg.strip(),settings.folder_events)

		# checks for pong response to our pings
		if ' ' in ircmsg and ircmsg.split(' ')[1] == 'PONG':
			self.conn.inc_precv()

		# executes commands from users
		if parser.is_command() and not parser.trigger_reload():
			self.irccommand(parser.get_command(), parser.get_cmdtext())

		# quits connections no longer in sockets list
		if self.conn not in self.connections:
			self.quit()

	def irccommand(self, cmd, cmdtext):
		cmd = cmd.lower().strip()
		cmdtext = cmdtext.strip()

		# checks for empty command
		if cmd.strip() == '':
			return

		# check for authorization
		if cmd in settings.cmds_secure and not self.auth():
			self.reply_safe(settings.msg_notauth)
			return

		# check for disabled commands
		if cmd in settings.cmds_disabled:
			self.reply_safe(settings.msg_disabled)
			return

		# execute the command
		if cmd in util.misc.cmds_normal():
			self.exec_cmd(cmd,cmdtext,settings.folder_mods)

		# attempts to account for typos
		else:
			match = util.misc.match_input(cmd,util.misc.cmds_all())
			if match != None:
				correct = match[0]
				cmdtext = match[1]+' '+cmdtext
				self.reply_safe('I\'ll interpret that command as \''+correct+'\'. Maybe you made a typo.')
				if correct != settings.cmd_reload:
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
		if modname in [settings.cmd_server, settings.cmd_quit]:
			mod.main(self, inputstr)
		else:
			if inputstr == None:
				p = multiprocessing.Process(target=mod.main,args=(self,))
			else:
				p = multiprocessing.Process(target=mod.main,args=(self,inputstr,))
			p.start()
			p.join()

def copy_bot(bot):
	copy = FlanBot()
	copy.connections = bot.connections
	copy.cparser = bot.cparser
	copy.conn = bot.conn
	return copy