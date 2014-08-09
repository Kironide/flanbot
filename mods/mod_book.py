import util, util.books
import settings

def main(cmdtext):
	sentence = util.books.random_sentence(cmdtext.split(' ')[0])
	if sentence != settings.msg_nobook:
		util.reply(sentence)
	else:
		util.reply_safe(sentence)