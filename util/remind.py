import timeutils, dataio, misc
import settings

# rdata stores the remind data
# dictionary with key = server, value = list of reminders on that server
# value = [#chan, time_from, time_send, sender, target, msg]

def load():
	return dataio.load_file(settings.datafile_remind,{})

def save(rdata):
	dataio.save_file(settings.datafile_remind,rdata)

# adds a reminder based on user input and then returns confirmation message
def add_reminder(serv, chan, tdest, sender, target, msg):
	if timeutils.validate(tdest):
		rdata = load()
		if serv not in rdata:
			rdata[serv] = []
		rdata[serv].append([chan,timeutils.now(),timeutils.parse(tdest),sender,target,msg])
		save(rdata)
		return('Okay, I\'ll remind '+target+' in '+timeutils.timediff(timeutils.parse(tdest))+'!')
	else:
		return ('Invalid input.')

def get_reminders(serv):
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