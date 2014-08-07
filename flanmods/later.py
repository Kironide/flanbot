import util

def main(cmdtext):
	if cmdtext[:5] == 'tell ':
		if len(cmdtext.split(' ')) < 3:
			util.reply_safe('Command has too few arguments.')
		else:
			irccommand(cmd, cmdtext[5:])
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
				add = util.later_add(later_nick, util.current_nick(), later_msg)
				if add:
					util.reply_safe('Message to '+later_nick+' recorded.')
				else:
					util.reply_safe('You\'ve already sent that message three times already.')