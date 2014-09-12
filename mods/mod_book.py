import util.books
import settings

def main(bot, cmdtext):
	sentence = util.books.random_sentence(cmdtext.split(' ')[0])
	if sentence != settings.msg_nobook:
		bot.reply(sentence)
	else:
		bot.reply_safe(sentence)