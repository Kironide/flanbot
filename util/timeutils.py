import time, math, parsedatetime
import settings

# returns the formatted time difference between a timestamp and current time
def timediff(ts):
	diff = math.fabs(int(time.time())- int(ts))
	if diff < 60:
		return str(int(diff))+'s'
	minutes = math.floor(diff/60.0)
	seconds = diff - minutes*60
	if minutes < 60:
		return str(int(minutes))+'m'+str(int(seconds))+'s'
	hours = math.floor(minutes/60.0)
	minutes = minutes - hours*60
	if hours < 24:
		return str(int(hours))+'h'+str(int(minutes))+'m'
	days = math.floor(hours/24.0)
	hours = hours - days*24
	return str(int(days))+'d'+str(int(hours))+'h'

# returns the current timestamp
def now():
	return time.time()

# returns timestamp corresponding to user input
def parse(text):
	cal = parsedatetime.Calendar()
	return time.mktime(cal.parse(text)[0])

# checks if input can be parsed properly
def validate(text):
	return isinstance((parsedatetime.Calendar()).parse(text)[0], time.struct_time)

# splits a string into a (time input,message) tuple and returns int
def split_input(text):
	ctime = time.gmtime(now())
	words = text.split(' ')
	if len(words) >= settings.time_parse_truncate:
		words_old = words[settings.time_parse_truncate:]
		words = words[:settings.time_parse_truncate]
	else:
		words_old = []
	prev = None
	prev_substr = ''
	fin = True
	for i in range(len(words)):
		substr = ' '.join(words[:len(words)-i])
		res = (parsedatetime.Calendar()).parse(substr,sourceTime=ctime)
		if prev == None:
			prev = res
		if prev != res:
			fin = False
			break
		prev_substr = substr
	if fin:
		return '',text
	else:
		return prev_substr,text.replace(prev_substr,'',1).strip()