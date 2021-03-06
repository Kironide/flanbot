import re, settings

def get_parser(ircmsg):
	return Parser(ircmsg)

class Parser:
	def __init__(self,ircmsg):
		try:
			self.ircmsg = ircmsg
			if ircmsg[0] != ':' or len(ircmsg.split(' ')) == 1:
				self.classification = 'self.other'
			else:
				halves = ['','']
				parts = ircmsg[1:].split(' ')
				hid = 0
				for pid in range(len(parts)):
					if parts[pid].startswith(':'):
						hid = 1
						parts[pid] = parts[pid][1:]
					halves[hid] = halves[hid]+' '+parts[pid]
				halves[0] = halves[0].strip()
				halves[1] = halves[1].strip()
				self.other = halves[0].split(' ')
				regex = re.compile('([^\s]+)![^a-zA-Z0-9]?([^\s]+)@([^\s]+)')
				r = regex.search(self.other[0])
				if r != None:
					self.classification = 'user'
					self.mask = self.other[0]
					self.nick = r.groups()[0]
					self.user = r.groups()[1]
					self.host = r.groups()[2]
					self.dtype = self.other[1]

					if self.dtype in ['NOTICE','QUIT','PART','PRIVMSG','MODE','KICK']:
						self.target = self.other[2]
					elif self.dtype == 'JOIN':
						self.target = halves[1]
					
					if self.dtype in ['NOTICE','QUIT','PART','PRIVMSG','QUIT','KICK']:
						self.text = halves[1]
					else:
						self.text = None
				else:
					self.classification = 'server'
					self.saddr = self.other[0]
					self.dtype = int(self.other[1])
					self.text = halves[1]
		except Exception, e:
			self.classification = 'self.other'

	def target_is_channel(self):
		return self.from_user() and self.target[0] in ['#','&']

	def from_server(self):
		return self.classification == 'server'
	def from_user(self):
		return self.classification == 'user'
	def from_self(self):
		return self.from_user() and self.nick.startswith(settings.botnick)

	def trigger_cmd(self):
		return self.from_user() and self.dtype == 'PRIVMSG'
	def trigger_later(self):
		return self.from_user() and self.dtype in ['PRIVMSG','JOIN']
	def trigger_seen(self):
		return self.from_user() and self.dtype in ['PRIVMSG','QUIT','PART','JOIN','NOTICE']
	def trigger_chaninfo(self):
		return self.from_user() and self.dtype in ['QUIT','PART','JOIN']
	def trigger_reload(self):
		return self.get_command() == settings.cmd_reload

	def is_command(self):
		return self.trigger_cmd() and self.text.startswith(settings.prefix)
	def get_command(self):
		return self.text.split(' ')[0][len(settings.prefix):]
	def get_cmdtext(self):
		return ' '.join(self.text.split(' ')[1:])

	def rpl_welcome(self):
		return self.from_server() and self.dtype == 1

	def rpl_namreply(self):
		return self.from_server() and self.dtype == 353
	def rpl_namreply_chan(self):
		return self.other[len(self.other)-1]
	def rpl_namreply_names(self):
		return self.text.split(' ')

	def err_nicknameinuse(self):
		return self.from_server() and self.dtype == 433
	def err_nicknameinuse_nick(self):
		return self.other[len(self.other)-1]

	def dtype_join(self):
		return self.from_user() and self.dtype == 'JOIN'
	def dtype_part(self):
		return self.from_user() and self.dtype == 'PART'
	def dtype_quit(self):
		return self.from_user() and self.dtype == 'QUIT'