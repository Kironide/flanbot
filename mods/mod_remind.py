import util.remind, util.timeutils

def main(bot, cmdtext):
	args = cmdtext.split(' ')
	if len(args) <= 2:
		bot.reply_safe('Not enough arguments.')
	else:
		target = args[0]
		if target.lower() == 'me':
			target = bot.current_nick()
		if args[1].lower() == 'in':
			args.remove('in')
		sinput = util.timeutils.split_input(' '.join(args[1:]))
		if sinput[0] == '':
			bot.reply_safe('Invalid time argument.')
		else:
			bot.reply(util.remind.add_reminder(bot.current_server(),bot.current_target(),sinput[0],bot.current_nick(),target,sinput[1]))