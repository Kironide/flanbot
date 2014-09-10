import util, util.remind, util.timeutils

def main(cmdtext):
	args = cmdtext.split(' ')
	if len(args) <= 2:
		util.reply_safe('Not enough arguments.')
	else:
		target = args[0]
		if args[1].lower() == 'in':
			args.remove('in')
		sinput = util.timeutils.split_input(' '.join(args[1:]))
		if sinput[0] == '':
			util.reply_safe('Invalid time argument.')
		else:
			util.reply(util.remind.add_reminder(util.current_server(),util.current_target(),sinput[0],util.current_nick(),args[0],sinput[1]))