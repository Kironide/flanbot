import timeutils
import settings
import os, pickle, time

# returns the pickled object in later.dat
# creates file with empty dict if it doesn't exist
# keys are usernames, values are lists of messages
# each message is stored as [timestamp, fromuser, msg]
def get_later():
	if not os.path.exists(settings.datafile_later):
		with open(settings.datafile_later,'w') as f:
			temp = {}
			pickle.dump(temp,f)
	with open(settings.datafile_later,'r') as f:
		temp = pickle.load(f)
	return temp

# save the later object to later.dat
def save_later(later):
	with open(settings.datafile_later,'w') as f:
		pickle.dump(later,f)

# adds a msg to send to the later object
# nick is the person to send to
# user is the person who sent it
def later_add(nick, user, msg):
	times = later_count(nick, user, msg)
	if times >= 3:
		return False
	later = get_later()
	if nick not in later:
		later[nick] = []
	later[nick].append([time.time(), user, msg])
	save_later(later)
	return True

# removes a user from the later object
def later_remove(nick):
	later = get_later()
	to_remove = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			to_remove.append(nick_later)
	for nick_later in to_remove:
		later.pop(nick_later, None)
	save_later(later)

# gets a list of messages to send for a certain nick
def later_read(nick):
	later = get_later()
	rawmsg = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for msg in msgs:
				rawmsg.append(msg)
	to_send = []
	for item in rawmsg:
		to_send.append(nick+': ('+timeutils.timediff(item[0])+') <'+item[1]+'> '+item[2])
	return to_send

# returns true if nick is in later
def later_contains(nick, later=None):
	if later == None:
		later = get_later()
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			return True
	return False

# number of times a message is recorded for someone
def later_count(nick, user, msg):
	later = get_later()
	times = 0
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for item in msgs:
				if msg == item[2] and user.lower() == item[1].lower():
					times += 1
	return times

# checks for msgs
def later_check(nick, later=None):
	if later == None:
		later = get_later()
	if later_contains(nick,later):
		messages = later_read(nick)
		later_remove(nick)
		return messages
	return []