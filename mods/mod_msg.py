def main(bot, cmdtext):
	recipient = cmdtext.split(' ')[0]
	message = ' '.join(cmdtext.split(' ')[1:])
	bot.send_msg(recipient, message)