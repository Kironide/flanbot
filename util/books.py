# utilities for dealing with books

import dataio
import ftfy, random
from textblob import TextBlob
import settings

# returns a random sentence
# returns 'I don't have that book on hand.' if it doesn't exist
def random_sentence(book):
	bookdata = dataio.load_raw(settings.folder_books+'/'+book+'.txt')
	if bookdata == None:
		return settings.msg_nobook
	blob = TextBlob(ftfy.fix_text(bookdata.decode('utf-8')))
	pos = random.randint(1,len(blob.sentences))-1
	return blob.sentences[pos:pos+settings.book_phrase_length]