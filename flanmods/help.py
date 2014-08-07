import util, settings

def main(cmdtext):
	cmds_all = util.cmds_all()

	if cmdtext == '':
		util.reply_safe('Currently available commands are: '+', '.join(cmds_all)+'. Type '+settings.prefix+'help [command] for a detailed description.')
	else:
		help_text = {
		'help': 'Syntax: help [optional: command]. Displays help.',
		'reload': 'Syntax: reload. Reloads bot functions.',
		'server': 'Syntax: server [address]. Connects to the specified server.',
		'quit': 'Syntax: quit [optional: message]. Disconnects from the current server.',
		'join': 'Syntax: join [channel] [optional: pass]. Joins the specified channel.',
		'part': 'Syntax: part [channel]. Parts the specified channel.',
		'later': 'Syntax: later [optional: tell] [nick] [message]. Leaves a message for [nick] when they join or say something.',
		'rthread': 'Syntax: rthread [optional: board]. Gets a random thread from a specified 4chan board or from a random board if unspecified.',
		'raw': 'Syntax: raw [data]. Sends data directly to the IRC socket.'
		}
		for cmd_temp,value in help_text.items():
			help_text[cmd_temp] = help_text[cmd_temp].replace('Syntax: ','Syntax: '+settings.prefix)
		help_cmd = cmdtext.split(' ')[0]
		if help_cmd in help_text:
			util.reply_safe(help_text[help_cmd])
		elif help_cmd not in cmds_all:
			util.reply_safe('That command does not exist.')
		else:
			util.reply_safe('Sorry, no help text has been set for that command yet.')