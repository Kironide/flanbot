import time, math

# returns the formatted time difference between a timestamp and current time
def timediff(ts):
	diff = int(time.time())- int(ts)
	if diff < 60:
		return str(diff)+'s ago'
	minutes = math.floor(diff/60.0)
	seconds = diff - minutes*60
	if minutes < 60:
		return str(int(minutes))+'m'+str(int(seconds))+'s ago'
	hours = math.floor(minutes/60.0)
	minutes = minutes - hours*60
	if hours < 24:
		return str(int(hours))+'h'+str(int(minutes))+'m ago'
	days = math.floor(hours/24.0)
	hours = hours - days*24
	return str(int(days))+'d'+str(int(hours))+'h ago'