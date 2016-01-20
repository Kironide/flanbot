def main(bot, cmdtext):
	messages = []
	temp = [x.upper() for x in list(cmdtext)]
	messages.append(' '.join(temp))

	for i in range(1, len(cmdtext) - 1):
		msg = cmdtext[i].upper() + ' ' * ((len(cmdtext) * 2) - 3) + cmdtext[-i-1].upper()
		messages.append(msg)

	temp.reverse()
	if len(cmdtext) > 1:
		messages.append(' '.join(temp))

	bot.reply_list(messages)