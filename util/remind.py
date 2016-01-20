import sqlite3, os
import timeutils, misc
import settings

# OLD DATA STRUCTURE:
# dictionary with key = server, value = list of reminders on that server
# value = [#chan, time_from, time_send, sender, target, msg]

# checks for existence of SQLite databases
def init():
	if not os.path.exists(settings.datafile_remind):
		c = sqlite3.connect(settings.datafile_remind)
		c.execute("CREATE TABLE remind (server text, channel text, time_start real, time_end real, nick_from text, nick_to text, msg text)")
		c.commit()
		c.close()

	if not os.path.exists(settings.datafile_remind + '.archive'):
		c = sqlite3.connect(settings.datafile_remind + '.archive')
		c.execute("CREATE TABLE remind (server text, channel text, time_start real, time_end real, nick_from text, nick_to text, msg text)")
		c.commit()
		c.close()

# adds a reminder based on user input and then returns confirmation message
def add_reminder(serv, chan, tdest, sender, target, msg):
	if timeutils.validate(tdest):
		current_time = timeutils.now()
		time_end = timeutils.parse(tdest)
		target = misc.sanitize_sql(target)
		msg = misc.sanitize_sql(msg)

		c = sqlite3.connect(settings.datafile_remind)
		c.execute("INSERT INTO remind VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}')".format(serv, chan, str(current_time), str(time_end), sender, target, msg))
		c.commit()
		c.close()

		c = sqlite3.connect(settings.datafile_remind + '.archive')
		c.execute("INSERT INTO remind VALUES ('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}')".format(serv, chan, str(current_time), str(time_end), sender, target, msg))
		c.commit()
		c.close()

		return('Okay, I\'ll remind '+target+' in '+timeutils.timediff(time_end)+'!')
	else:
		return ('Invalid input.')

# get a list of reminders for a specific server that have to be delivered
def get_reminders(serv):
	init()

	queue = []
	current_time = timeutils.now()
	c = sqlite3.connect(settings.datafile_remind)
	for row in c.execute("SELECT * FROM remind WHERE server = '{0}' AND time_end <= {1}".format(serv, str(current_time))):
		reminder = [row[1], float(row[2]), float(row[3]), row[4], row[5], row[6]]
		queue.append(reminder)
	c.execute("DELETE FROM remind WHERE server = '{0}' AND time_end <= {1}".format(serv, str(current_time)))
	c.commit()
	c.close()
	return queue

# list nicks that have pending messages to/from them
def list_nicks(serv, chan):
	nicks = []
	c = sqlite3.connect(settings.datafile_remind)
	for row in c.execute("SELECT DISTINCT nick_from FROM remind WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		nicks.append(row[0])
	for row in c.execute("SELECT DISTINCT nick_to FROM remind WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		nicks.append(row[0])
	c.close()
	nicks = list(set(nicks))
	nicks.sort()
	to_remove = []
	for n in nicks:
		if n.lower() in nicks:
			to_remove.append(n.lower())
	to_remove = set(to_remove)
	for x in to_remove:
		nicks.remove(x)
	return nicks

# reads remind msgs from specific user
def read_from(serv, chan, nick_from):
	messages = []

	c = sqlite3.connect(settings.datafile_remind)
	for row in c.execute("SELECT * FROM remind WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		if nick_from.lower() == row[4].lower():
			time_diff = timeutils.timediff(float(row[3]))
			messages.append(u"{0} to {1} (in {2}): {3}".format(row[4], row[5], time_diff, row[6]))
	c.close()

	return messages

# reads remind msgs to specific user
def read_to(serv, chan, nick_to):
	messages = []

	c = sqlite3.connect(settings.datafile_remind)
	for row in c.execute("SELECT * FROM remind WHERE server = '{0}' AND channel = '{1}'".format(serv, chan)):
		if nick_to.lower() == row[5].lower():
			time_diff = timeutils.timediff(float(row[3]))
			messages.append(u"{0} to {1} (in {2}): {3}".format(row[4], row[5], time_diff, row[6]))
	c.close()

	return messages