import util.remind, util.timeutils

def main(bot, cmdtext):
	args = cmdtext.split(' ')
	if len(args) <= 1:
		bot.reply_safe('Not enough arguments.')
	elif cmdtext.startswith('view'):
		if len(cmdtext.split(' ')) == 1:
			valid_users = util.remind.list_nicks(bot.current_server(), bot.current_target())
			if len(valid_users) > 0:
				bot.reply_safe("Nicks associated with this channel have been privately messaged to you.")
				bot.reply_notice("Nicks associated with this channel: " + ', '.join(valid_users))
			else:
				bot.reply_safe("No nicks associated with this channel.")
		elif len(cmdtext.split(' ')) == 3:
			cmd, choice, nick = cmdtext.split(' ')
			if choice not in ("from", "to"):
				bot.reply_safe("The second argument must be either 'from' or 'to'.")
			else:
				if choice == "from":
					messages = util.remind.read_from(bot.current_server(), bot.current_target(), nick)
				elif choice == "to":
					messages = util.remind.read_to(bot.current_server(), bot.current_target(), nick)
				if len(messages) == 0:
					bot.reply_safe("No messages to show for {0}.".format(nick))
				else:
					max_count = len(messages)
					for i in range(len(messages)):
						messages[i] = "[{0}/{1}] ".format(str(i+1), str(max_count)) + messages[i]
					bot.reply_list(messages)
					bot.reply_safe("I'm done listing messages {0} {1}.".format(choice, nick))
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