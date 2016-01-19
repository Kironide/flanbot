import sqlite3, os
import timeutils, dataio, misc
import settings

def init():
	if not os.path.exists(settings.datafile_later):
		c = sqlite3.connect(settings.datafile_later)
		c.execute("CREATE TABLE later (server text, channel text, time text, nick_from text, nick_to text, msg text)")
		c.commit()
		c.close()

	if not os.path.exists(settings.datafile_later + '.archive'):
		c = sqlite3.connect(settings.datafile_later + '.archive')
		c.execute("CREATE TABLE later (server text, channel text, time text, nick_from text, nick_to text, msg text)")
		c.commit()
		c.close()

# adds a msg to send to the later object
def add(serv, chan, nick_from, nick_to, msg):
	nick_to = nick_to.lower()
	times = count(serv, chan, nick_from, nick_to, msg)
	if times >= 3:
		return False

	c = sqlite3.connect(settings.datafile_later)
	c.execute("INSERT INTO later VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(serv, chan, str(timeutils.now()), nick_from, nick_to.lower(), msg))
	c.commit()
	c.close()

	c = sqlite3.connect(settings.datafile_later + '.archive')
	c.execute("INSERT INTO later VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(serv, chan, str(timeutils.now()), nick_from, nick_to.lower(), msg))
	c.commit()
	c.close()

	return True

# removes a server/channel/nick combination
def remove(serv, chan, nick):
	c = sqlite3.connect(settings.datafile_later)
	c.execute("DELETE FROM later WHERE server = '{0}' AND channel = '{1}' AND nick_to = '{2}'".format(serv, chan, nick.lower()))
	c.commit()
	c.close()

# gets a list of messages to send for a certain server/channel/nick combination
def read(serv, chan, nick):
	to_send = []

	c = sqlite3.connect(settings.datafile_later)
	for row in c.execute("SELECT * FROM later WHERE server = '{0}' AND channel = '{1}' AND nick_to = '{2}'".format(serv, chan, nick.lower())):
		timestamp, nick_from, msg = float(row[2]), row[3], row[5]
		to_send.append("{0}: ({1} ago) <{2}> {3}".format(nick, timeutils.timediff(timestamp), nick_from, msg))
	c.close()

	return to_send

# returns true if server/channel/nick is in later
def later_contains(serv, chan, nick):
	c = sqlite3.connect(settings.datafile_later)
	for row in c.execute("SELECT * FROM later WHERE server = '{0}' AND channel = '{1}' AND nick_to = '{2}'".format(serv, chan, nick.lower())):
		return True
	c.close()
	return False

# number of times a message is recorded for someone
def count(serv, chan, nick_from, nick_to, msg):
	times = 0

	c = sqlite3.connect(settings.datafile_later)
	for row in c.execute("SELECT * FROM later WHERE server = '{0}' AND channel = '{1}' AND nick_to = '{2}' AND msg = '{3}'".format(serv, chan, nick_to.lower(), msg)):
		if nick_from.lower() == row[3].lower():
			times += 1
	c.close()

	return times

# checks for msgs
def check(serv, chan, nick):
	init()
	if later_contains(serv, chan, nick):
		messages = read(serv, chan, nick)
		remove(serv, chan, nick)
		return messages
	return []

# list of nicks for given serv/chan
def list_nicks(serv, chan):
	nicks = []
	c = sqlite3.connect(settings.datafile_later)
	for row in c.execute("SELECT DISTINCT nick_from FROM later WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		nicks.append(row[0])
	for row in c.execute("SELECT DISTINCT nick_to FROM later WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		nicks.append(row[0])
	c.close()
	nicks = list(set(nicks))
	nicks.sort()
	return nicks

# reads msgs from specific user
def read_from(serv, chan, nick_from):
	messages = []

	c = sqlite3.connect(settings.datafile_later)
	for row in c.execute("SELECT * FROM later WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		if nick_from.lower() == row[3].lower():
			time_diff = timeutils.timediff(float(row[2]))
			messages.append(u"{0} to {1} ({2}): {3}".format(row[3].encode("utf-8"), row[4].encode("utf-8"), time_diff, row[5].encode("utf-8")).encode("utf-8"))
	c.close()

	return messages

# reads msgs to specific user
def read_to(serv, chan, nick_to):
	messages = []

	c = sqlite3.connect(settings.datafile_later)
	for row in c.execute("SELECT * FROM later WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		if nick_to.lower() == row[4].lower():
			time_diff = timeutils.timediff(float(row[2]))
			messages.append(u"{0} to {1} ({2}): {3}".format(row[3].encode("utf-8"), row[4].encode("utf-8"), time_diff, row[5].encode("utf-8")).encode("utf-8"))
	c.close()

	return messages