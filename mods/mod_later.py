import util.later, util.chaninfo, util.misc

def main(bot, cmdtext, retry=False):
	if cmdtext[:5] == 'tell ':
		if len(cmdtext.split(' ')) < 3:
			bot.reply_safe('Command has too few arguments.')
		else:
			main(bot, cmdtext[5:])
	else:
		if len(cmdtext.split(' ')) < 2:
			bot.reply_safe('Command has too few arguments.')
		else:
			temp = cmdtext.split(' ')
			later_nick = temp[0]
			if len(later_nick) >= 3 and later_nick[:3].lower() == 'xpc':
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