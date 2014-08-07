import os, pickle, time, math

# returns just the nick from stuff!idk@whatever
def get_nick(user):
	return user.split('!')[0].replace(':','')

# returns the formatted time difference between a timestamp and current time
def timediff(ts):
	diff = int(time.time())- int(ts)
	if diff < 60:
		return str(diff)+'s ago'
	minutes = math.floor(diff/60.0)
	seconds = diff - minutes*60
	if minutes < 60:
		return str(int(minutes))+'m'+str(int(seconds))+'s ago'
	hours = math.floor(minutes/60.0)
	minutes = minutes - hours*60
	if hours < 24:
		return str(int(hours))+'h'+str(int(minutes))+'m ago'
	days = math.floor(hours/24.0)
	hours = hours - days*24
	return str(int(days))+'d'+str(int(hours))+'h ago'

#########################
# IRC NETWORK FUNCTIONS #
#########################

######################################
# STUFF RELATED TO THE LATER COMMAND #
######################################

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
	times = count_later(nick, user, msg)
	if times >= 3:
		return False
	later = get_later()
	if nick not in later:
		later[nick] = []
	later[nick].append([time.time(), user, msg])
	save_later(later)
	return True

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
		##to_send.append(nick+': ['+datetime.datetime.fromtimestamp(int(item[0])).strftime('%Y-%m-%d %H:%M:%S')+']<'+item[1]+'> '+item[2])
		to_send.append(nick+': ('+timediff(item[0])+') <'+item[1]+'> '+item[2])
	return to_send

# returns true if nick is in later
def in_later(nick, later=None):
	if later == None:
		later = get_later()
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			return True
	return False

# number of times a message is recorded for someone
def count_later(nick, user, msg):
	later = get_later()
	times = 0
	for nick_later,msgs in later.items():
		if nick.lower() == nick_later.lower():
			for item in msgs:
				if msg == item[2] and user.lower() == item[1].lower():
					times += 1
	return times

#####################################
# STUFF RELATED TO THE SEEN COMMAND #
#####################################

# save data about someone
def save_seen(nick, type, msg=''):
	# create data file if it doesn't exist
	if not os.path.exists('seen.dat'):
		with open('seen.dat','w') as f:
			test = 1