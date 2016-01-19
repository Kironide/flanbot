import time
import util.later, util.chaninfo, util.misc

def main(bot, cmdtext, retry=False):
	if cmdtext[:5] == 'tell ':
		if len(cmdtext.split(' ')) < 3:
			bot.reply_safe('Command has too few arguments.')
		else:
			main(bot, cmdtext[5:])
	elif cmdtext.startswith('view'):
		if len(cmdtext.split(' ')) == 1:
			valid_users = util.later.list_nicks(bot.current_server(), bot.current_target())
			if len(valid_users) > 0:
				bot.reply_safe("Nicks associated with this channel: " + ', '.join(valid_users))
			else:
				bot.reply_safe("No nicks associated with this channel.")
		elif len(cmdtext.split(' ')) == 3:
			cmd, choice, nick = cmdtext.split(' ')
			if choice not in ("from", "to"):
				bot.reply_safe("The second argument must be either 'from' or 'to'.")
			else:
				if choice == "from":
					messages = util.later.read_from(bot.current_server(), bot.current_target(), nick)
				elif choice == "to":
					messages = util.later.read_to(bot.current_server(), bot.current_target(), nick)
				if len(messages) == 0:
					bot.reply_safe("No messages to show.")
				else:
					max_count = len(messages)
					for i in range(len(messages)):
						messages[i] = "({0}/{1}) ".format(str(i+1), str(max_count)) + m
					bot.reply_list(messages)
					bot.reply_safe("I'm done listing messages {0} {1}.".format(choice, nick))

		else:
			bot.reply_safe('Command has incorrect number of arguments.')
	else:
		if len(cmdtext.split(' ')) < 2:
			bot.reply_safe('Command has too few arguments.')
		else:
			temp = cmdtext.split(' ')
			later_nick = temp[0]
			if len(later_nick) >= 3 and later_nick[:3].lower() == 'xpc' and not bot.current_nick().startswith('xpc'):
				bot.reply_safe('You know he doesn\'t like that.')
				return False
			else:
				add_retry = None
				later_msg = ' '.join(temp[1:])
				chan_nicks = util.chaninfo.get_users(bot.current_server(),bot.current_target())
				if bot.cparser.target_is_channel() and later_nick.lower() not in [x.lower() for x in chan_nicks]:
					match = util.misc.match_input_weak(later_nick,chan_nicks)
					if match != None and later_nick.lower() != match.lower():
						bot.reply('Did you mean to send that to '+match+'? I\'ll send it as well just in case.')
						add_retry = util.later.add(bot.current_server(), bot.current_target(), bot.current_nick(), match, later_msg)
				add = util.later.add(bot.current_server(), bot.current_target(), bot.current_nick(), later_nick, later_msg)
				if add and add_retry == True:
					bot.reply_safe('Messages to '+later_nick+' and '+match+' recorded.')
					return
				if not add and add_retry == False:
					bot.reply_safe('You\'ve already sent that message to both'+later_nick+' and '+match+' three times already.')
					return
				if add:
					if add_retry == False:
						bot.reply_safe('Message to '+later_nick+' recorded, but you\'ve already sent that to '+match+' three times already.')
					elif add_retry == None:
						bot.reply_safe('Message to '+later_nick+' recorded.')
				else:
					if add_retry == True:
						bot.reply_safe('You\'ve already sent that message to '+later_nick+' three times already, but your message to '+match+' has been recorded.')
					elif add_retry == None:
						bot.reply_safe('You\'ve already sent that message to '+later_nick+' three times already.')