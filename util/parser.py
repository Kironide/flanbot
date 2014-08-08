import re, settings

def get_parser(ircmsg):
	return Parser(ircmsg)

class Parser:
	def __init__(self,ircmsg):
		try:
			if ircmsg[0] != ':' or len(ircmsg.split(' ')) == 1:
				self.classification = 'other'
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
				other = halves[0].split(' ')
				regex = re.compile('([^\s]+)![^a-zA-Z0-9]?([^\s]+)@([^\s]+)')
				r = regex.search(other[0])
				if r != None:
					self.classification = 'user'
					self.mask = other[0]
					self.nick = r.groups()[0]
					self.user = r.groups()[1]
					self.host = r.groups()[2]
					self.dtype = other[1]

					if self.dtype in ['NOTICE','QUIT','PART','PRIVMSG','MODE','KICK']:
						self.target = other[2]
					elif self.dtype == 'JOIN':
						self.target = halves[1]
					
					if self.dtype in ['NOTICE','QUIT','PART','PRIVMSG','QUIT','KICK']:
						self.text = halves[1]
					else:
						self.text = None
				else:
					self.classification = 'server'
					self.saddr = other[0]
					self.dtype = int(other[1])
		except Exception, e:
			print(e)
			self.classification = 'other'

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

	def is_command(self):
		return self.trigger_cmd() and self.text.startswith(settings.prefix)
	def get_command(self):
		return self.text.split(' ')[0][len(settings.prefix):]
	def get_cmdtext(self):
		return ' '.join(self.text.split(' ')[1:])

	def err_nicknameinuse(self):
		return self.from_server() and self.dtype == 433