import util

def main(cmdtext):
	if cmdtext.split(' ')[0].lower() == '#dontjoinitsatrap':
		util.reply_safe('Nice try, nerd.')
	else:
		util.joinchan(cmdtext.strip())