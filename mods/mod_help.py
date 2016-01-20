import util.misc
import settings

def main(bot, cmdtext):
	cmds_all = util.misc.cmds_all()

	if cmdtext == "":
		bot.reply_notice("Currently available commands are: "+", ".join(cmds_all)+". Type "+settings.prefix+"help [command] for a detailed description.")
	else:
		help_text = {
		"help":			"Syntax: help [optional: command]. Displays help."
		,"reload":		"Syntax: reload. Reloads bot functions."
		,"server":		"Syntax: server [address]. Connects to the specified server."
		,"quit":		"Syntax: quit [optional: message]. Disconnects from the current server."
		,"join":		"Syntax: join [channel] [optional: pass]. Joins the specified channel."
		,"part":		"Syntax: part [optional: channel]. Parts the specified channel or the current channel if unspecified."
		,"later":		"Syntax: later [optional: 'tell'] [nick] [message]. Leaves a message for [nick] when they join or say something. To view queued messages, use 'later view' to display a list of valid nicks and 'later view [to/from] [nick] to display associated messages."
		,"rthread":		"Syntax: rthread [optional: board]. Gets a random thread from a specified 4chan board or from a random board if unspecified."
		,"raw":			"Syntax: raw [data]. Sends data directly to the IRC socket."
		,"joininit":	"Syntax: joininit. Rejoins the channels specified in the settings."
		,"server":		"Syntax: server [server]. Connects to the specified server."
		,"quit":		"Syntax: quit. Disconnects from the current server."
		,"test":		"Syntax: depends. This does various things at various times."
		,"dice":		"Syntax: [optional: NdM]. Rolls a dice and defaults to 1d6 if not specified."
		,"book":		"Syntax: book [book]. Returns a random sentence from a book. Available books: "+", ".join(util.misc.books_all())
		,"remind":		"Syntax: remind [nick] [optional: 'in'] [time] [message]. Sends a message to the specified nick at a later time. To view queued messages, use 'remind view' to display a list of valid nicks and 'remind view [to/from] [nick] to display associated messages."
		}
		for cmd_temp,value in help_text.items():
			help_text[cmd_temp] = help_text[cmd_temp].replace("Syntax: ","Syntax: "+settings.prefix)
		help_cmd = cmdtext.split(" ")[0]
		if help_cmd in help_text:
			bot.reply_notice(help_text[help_cmd])
		elif help_cmd not in cmds_all:
			bot.reply_notice("That command does not exist.")
		else:
			bot.reply_notice("Sorry, no help text has been set for that command yet.")