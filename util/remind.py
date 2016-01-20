import sqlite3, os
import timeutils
import settings

def init():
	if not os.path.exists(settings.datafile_remind):
		c = sqlite3.connect(settings.datafile_remind)
		c.execute("CREATE TABLE remind (server text, channel text, time_from text, duration text, nick_from text, nick_to text, msg text)")
		c.commit()
		c.close()

# rdata stores the remind data
# dictionary with key = server, value = list of reminders on that server
# value = [#chan, time_from, time_send, sender, target, msg]

# adds a reminder based on user input and then returns confirmation message
def add_reminder(serv, chan, tdest, sender, target, msg):
	if timeutils.validate(tdest):
		current_time = str(timeutils.now())
		duration = timeutils.parse(tdest)
		target = misc.sanitize_sql(target)
		msg = misc.sanitize_sql(msg)

		c = sqlite3.connect(settings.datafile_remind)
		c.execute("INSERT INTO remind VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(serv, chan, current_time, duration, sender, target, msg))
		c.commit()
		c.close()

		return('Okay, I\'ll remind '+target+' in '+timeutils.timediff(duration)+'!')
	else:
		return ('Invalid input.')

def get_reminders(serv):
	init()
	
	c = sqlite3.connect(settings.datafile_remind)
	if


	rdata = load()
	if serv not in rdata:
		return []
	queue = []
	now = timeutils.now()
	for reminder in rdata[serv]:
		if now >= reminder[2]:
			queue.append(reminder)
	for r in queue:
		rdata[serv].remove(r)
	save(rdata)
	return queue