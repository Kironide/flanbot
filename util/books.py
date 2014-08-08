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
		return 'I don\'t have that book on hand.'
	blob = TextBlob(ftfy.fix_text(bookdata.decode('utf-8')))
	return blob.sentences[random.randint(1,len(blob.sentences))-1]