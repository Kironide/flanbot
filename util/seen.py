import timeutils, dataio
import settings
import os, pickle

def load():
	return dataio.load_file(settings.datafile_seen,{})

def save(seen_data):
	dataio.save_file(settings.datafile_seen,seen_data)

# save data about someone in dict
# removes the last entry in the list and appends new data to the front
# each item is of form [dtype,target,msg]
def seen_save(ts, nick, dtype, target, msg):
	# store all nicks in lowercase form
	nick = nick.lower()

	# load seen data
	seen_data = load()

	# if nick isn't in the data, then create an empty entry
	if nick not in seen_data:
		seen_data[nick] = [None]*settings.seen_buffer

	if len(seen_data[nick]) > settings.seen_buffer:
		for i in range(len(seen_data[nick]) - settings.seen_buffer):
			seen_data[nick].pop()
	elif len(seen_data[nick]) < settings.seen_buffer:
		for i in range(settings.seen_buffer - len(seen_data[nick])):
			seen_data[nick].append(None)

	# put the data in
	seen_data[nick].pop()
	item = [ts,dtype,target,msg]
	seen_data[nick].insert(0,item)

	# save it
	save(seen_data)

# converts a [timestamp, dtype,target,msg] list to a phrase
def seen_dataconv(data):
	(ts,dtype,target,msg) = data
	tdelta = timeutils.timediff(ts)
	if dtype == 'PART':
		msg = 'parting '+target
	elif dtype == 'JOIN':
		msg = 'joining '+target
	elif dtype == 'PRIVMSG' or dtype == 'NOTICE':
		msg = 'saying "'+msg+'" in '+target
	elif dtype == 'QUIT':
		msg = 'quitting'
	msg = msg+' '+tdelta
	return msg

# returns things to say about a user
def seen_lookup(nick):
	nick = nick.lower()
	seen_data = load()
	if nick not in seen_data:
		return 'That user has never been seen before.'
	rawdata = seen_data[nick]
	while None in rawdata:
		rawdata.remove(None)
	msg = nick+' was last seen '
	if len(rawdata) == 1:
		msg = msg+seen_dataconv(rawdata[0])
	elif len(rawdata) == 2:
		msg = msg+seen_dataconv(rawdata[0])+' and '+seen_dataconv(rawdata[1])
	elif len(rawdata) >= 3:
		msg = msg+', '.join([seen_dataconv(x) for x in rawdata[:len(rawdata)-1]])+', and '+seen_dataconv(rawdata[len(rawdata)-1])
	msg = msg+'.'
	return msg