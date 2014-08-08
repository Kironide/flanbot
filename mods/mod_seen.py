import util
import util.seen

def main(cmdtext):
	nick = cmdtext.split(' ')[0]
	util.reply_safe(util.seen.seen_lookup(nick))