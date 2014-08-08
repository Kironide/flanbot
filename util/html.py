import HTMLParser, requests
from BeautifulSoup import BeautifulSoup as bs4

# return the HTML from an URL
def get_url(url):
	s = requests.Session()
	return s.get(url).text

# strip tags from HTML content
def strip_tags(html):
	return ''.join(bs4(html).findAll(text=True))

# formats html entitites
def format_entities(html):
	h = HTMLParser.HTMLParser()
	return h.unescape(html)