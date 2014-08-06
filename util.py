import os, pickle, time

def get_nick(user):
	return user.split('!')[0].replace(':','')

# returns the pickled object in later.dat
# creates file with empty dict if it doesn't exist
# keys are usernames, values are lists of messages
# each message is stored as [timestamp, fromuser, msg]
def get_later():
	if not os.path.exists('later.dat'):
		with open('later.dat','w') as f:
			temp = {}
			pickle.dump(temp,f)
	with open('later.dat','r') as f:
		temp = pickle.load(f)
	return temp

# save the later object to later.dat
def save_later(later):
	with open('later.dat','w') as f:
		pickle.dump(later,f)

# adds a msg to send to the later object
# nick is the person to send to
# user is the person who sent it
def add_later(nick, user, msg):
	later = get_later()
	if nick not in later:
		later[nick] = []
	later[nick].append([time.time(), user, msg])
	save_later(later)

# removes a user from the later object
def remove_later(nick):
	later = get_later()
	to_remove = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			to_remove.append(nick_later)
	for nick_later in to_remove:
		later.pop(nick_later, None)
	save_later(later)

# gets a list of messages to send for a certain nick
def read_later(nick):
	later = get_later()
	rawmsg = []
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for msg in msgs:
				rawmsg.append(msg)
	to_send = []
	for item in rawmsg:
		to_send.append(nick+': <'+item[1]+'> '+item[2])
	return to_send

# returns true if nick is in later
def in_later(nick, later=None):
	if later == None:
		later = get_later()
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			return True
	return False