import util, util.later, util.chaninfo, util.misc

def main(cmdtext):
	if cmdtext[:5] == 'tell ':
		if len(cmdtext.split(' ')) < 3:
			util.reply_safe('Command has too few arguments.')
		else:
			main(cmdtext[5:])
	else:
		if len(cmdtext.split(' ')) < 2:
			util.reply_safe('Command has too few arguments.')
		else:
			temp = cmdtext.split(' ')
			later_nick = temp[0]
			if len(later_nick) >= 3 and later_nick[:3].lower() == 'xpc':
				util.reply_safe('You know he doesn\'t like that.')
			else:
				later_msg = ' '.join(temp[1:])
				chan_nicks = util.chaninfo.get_users(util.current_server(),util.current_target())
				if util.cparser.target_is_channel() and later_nick not in chan_nicks:
					match = util.misc.match_input_weak(later_nick,chan_nicks)
					if match != None and later_nick.lower() != match.lower():
						util.reply('Did you mean to send that to '+match+'? I\'ll send it as well just in case.')
						main('tell '+match+' '+later_msg)

				add = util.later.add(later_nick, util.current_nick(), later_msg)
				if add:
					util.reply_safe('Message to '+later_nick+' recorded.')
				else:
					util.reply_safe('You\'ve already sent that message three times already.')