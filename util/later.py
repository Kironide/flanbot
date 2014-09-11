import timeutils, dataio, misc
import settings

# returns the pickled object in later.dat
# creates file with empty dict if it doesn't exist
# keys are usernames, values are lists of messages
# each message is stored as [timestamp, fromuser, msg]
def load():
	return dataio.load_file(settings.datafile_later,{})

# save the later object to later.dat
def save(later):
	dataio.save_file(settings.datafile_later,later)

# adds a msg to send to the later object
def add(serv, chan, nick_from, nick_to, msg):
	nick_to = nick_to.lower()
	times = count(serv, chan, nick_from, nick_to, msg)
	if times >= 3:
		return False
	later = load()
	if serv not in later:
		later[serv] = {}
	if chan not in later[serv]:
		later[serv][chan] = {}
	if nick_to not in later[serv][chan]:
		later[serv][chan][nick_to] = []
	later[serv][chan][nick_to].append({'time': timeutils.now(), 'from': nick_from, 'msg': msg})
	save(later)
	return True

# removes a server/channel/nick combination
def remove(serv, chan, nick):
	later = load()
	if serv in later:
		if chan in later[serv]:
			if nick.lower() in later[serv][chan]:
				later[serv][chan].pop(nick.lower(), None)
	save(later)

# gets a list of messages to send for a certain server/channel/nick combination
def read(serv, chan, nick):
	later = load()
	to_send = []
	if serv in later:
		if chan in later[serv]:
			if nick.lower() in later[serv][chan]:
				for msg in later[serv][chan][nick.lower()]:
					to_send.append(''+nick+': ('+timeutils.timediff(msg['time'])+' ago) <'+msg['from']+'> '+msg['msg'])
	return to_send

# returns true if server/channel/nick is in later
def later_contains(serv, chan, nick):
	later = load()
	if serv in later:
		if chan in later[serv]:
			if nick.lower() in later[serv][chan]:
				return True
	return False

# number of times a message is recorded for someone
def count(serv, chan, nick_from, nick_to, msg):
	later = load()
	times = 0
	if serv in later:
		if chan in later[serv]:
			if nick_to in later[serv][chan]:
				for item in later[serv][chan][nick_to]:
					if item['msg'] == msg and item['from'].lower() == nick_from.lower():
						times += 1
	return times

# checks for msgs
def check(serv, chan, nick):
	if later_contains(serv, chan, nick):
		messages = read(serv, chan, nick)
		remove(serv, chan, nick)
		messages.reverse()
		return messages
	return []