import HTMLParser
from BeautifulSoup import BeautifulSoup as bs4

# strip tags from HTML content
def strip_tags(html):
	return ''.join(bs4(html).findAll(text=True))

# formats html entitites
def format_entities(html):
	h = HTMLParser.HTMLParser()
	return h.unescape(html)