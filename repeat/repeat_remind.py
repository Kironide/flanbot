import util, util.remind, util.timeutils

def main():
	reminders = util.remind.get_reminders(util.current_server())
	for r in reminders:
		util.sendmsg(r[0],''+r[4]+':'+' ('+util.timeutils.timediff(r[1])+' ago) <'+r[3]+'> '+r[5])