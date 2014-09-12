import util.remind, util.timeutils

def main(bot):
	reminders = util.remind.get_reminders(bot.current_server())
	for r in reminders:
		bot.send_msg(r[0],''+r[4]+':'+' ('+util.timeutils.timediff(r[1])+' ago) <'+r[3]+'> '+r[5])