import sqlite3, os
import timeutils, misc
import settings

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

# rdata stores the remind data
# dictionary with key = server, value = list of reminders on that server
# value = [#chan, time_from, time_send, sender, target, msg]

# adds a reminder based on user input and then returns confirmation message
def add_reminder(serv, chan, tdest, sender, target, msg):
	if timeutils.validate(tdest):
		current_time = timeutils.now()
		time_end = timeutils.parse(tdest)
		duration = time_end - current_time
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

		return('Okay, I\'ll remind '+target+' in '+timeutils.timediff(duration)+'!')
	else:
		return ('Invalid input.')

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