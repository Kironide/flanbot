def main(bot, cmdtext):
	if cmdtext.split(' ')[0].lower() == '#dontjoinitsatrap':
		bot.reply_safe('Nice try, nerd.')
	else:
		bot.join(cmdtext)