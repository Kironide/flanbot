def main(bot, cmdtext):
	if cmdtext == '':
		if bot.cparser.target_is_channel():
			bot.part(bot.current_target())
	else:
		bot.part(cmdtext.split(' ')[0])