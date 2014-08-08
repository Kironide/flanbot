import util, util.books

def main(cmdtext):
	util.reply(util.books.random_sentence(cmdtext.split(' ')[0]))