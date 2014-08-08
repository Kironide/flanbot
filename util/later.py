import timeutils, dataio, misc
import settings
import os, pickle, time

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
# nick is the person to send to
# user is the person who sent it
def add(nick, user, msg):
	times = count(nick, user, msg)
	if times >= 3:
		return False
	later = load()
	if nick not in later:
		later[nick] = []
	later[nick].append([time.time(), user, msg])
	save(later)
	return True

# removes a user from the later object
def remove(nick):
	later = load()
	to_remove = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			to_remove.append(nick_later)
	for nick_later in to_remove:
		later.pop(nick_later, None)
	save(later)

# gets a list of messages to send for a certain nick
def read(nick):
	later = load()
	rawmsg = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for msg in msgs:
				rawmsg.append(msg)
	to_send = []
	for item in rawmsg:
		to_send.append(''+nick+': ('+timeutils.timediff(item[0])+') <'+item[1]+'> '+item[2])
	return to_send

# returns true if nick is in later
def later_contains(nick, later=None):
	if later == None:
		later = load()
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			return True
	return False

# number of times a message is recorded for someone
def count(nick, user, msg):
	later = load()
	times = 0
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for item in msgs:
				if msg == item[2] and user.lower() == item[1].lower():
					times += 1
	return times

# checks for msgs
def check(nick, later=None):
	if later == None:
		later = load()
	if later_contains(nick,later):
		messages = read(nick)
		remove(nick)
		messages.reverse()
		return messages
	return []