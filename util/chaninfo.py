# utilities for recording the nicks in a channel

import dataio
import settings

# returns the chaninfo data file
# dictionary with servers as the keys
# each dictionary entry is a dictionary of channels -> lists of users
def load():
	return dataio.load_file(settings.datafile_chaninfo,{})

# save chaninfo to file
def save(cinfo):
	dataio.save_file(settings.datafile_chaninfo,cinfo)

# adds a channel to chaninfo file
def add_channel(serv,chan,nicks):
	cinfo = load()
	if serv not in cinfo:
		cinfo[serv] = {}
	cinfo[serv][chan] = nicks
	save(cinfo)

# removes a nick from a server's channels
def remove_nick_serv(serv,nick):
	cinfo = load()
	if serv in cinfo:
		for chan in list(cinfo[serv].keys()):
			if nick in cinfo[serv][chan]:
				cinfo[serv][chan].remove(nick)
	save(cinfo)

# removes a nick from a specific serv/chan combination
def remove_nick_chan(serv,chan,nick):
	cinfo = load()
	if serv in cinfo:
		if chan in cinfo[serv]:
			if nick in cinfo[serv][chan]:
				cinfo[serv][chan].remove(nick)
	save(cinfo)

# adds a nick to a specific serv/chan combination
def add_nick_chan(serv,chan,nick):
	cinfo = load()
	if serv in cinfo:
		if chan in cinfo[serv]:
			if nick not in cinfo[serv][chan]:
				cinfo[serv][chan].append(nick)
	save(cinfo)

# gets the userlist for a serv/chan combination
def get_users(serv,chan):
	cinfo = load()
	if serv in cinfo:
		if chan in cinfo[serv]:
			return cinfo[serv][chan]
	return []