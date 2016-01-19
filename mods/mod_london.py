def main(bot, cmdtext):
	messages = []
	temp = [x.upper() for x in list(cmdtext)]
	messages.append(' '.join(temp))

	for i in range(1, len(cmdtext) - 2):
		msg = cmdtext[i].upper() + ' ' * (len(cmdtext) - 2) + cmdtext[-i].upper()
		messages.append(msg)

	temp.reverse()
	messages.append(' '.join(temp))

	bot.reply_list(messages)