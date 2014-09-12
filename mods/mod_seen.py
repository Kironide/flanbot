import util.seen

def main(bot, cmdtext):
	nick = cmdtext.split(' ')[0]
	bot.reply_safe(util.seen.seen_lookup(nick))