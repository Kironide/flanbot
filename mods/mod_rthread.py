import util, util.html
import requests, json, random

def main(cmdtext):
	s = requests.Session()
	if cmdtext == '':
		boards = json.loads(s.get('http://a.4cdn.org/boards.json').text)['boards']
		rboard = boards[random.randint(1,len(boards))-1]['board']
		main(rboard)
	else:
		try:
			cat = json.loads(s.get('http://a.4cdn.org/'+cmdtext.split(' ')[0]+'/catalog.json').text)
			threads = []
			for page in cat:
				for thread in page['threads']:
					threads.append(thread)
			rthread = threads[random.randint(1,len(threads))-1]
			if 'sub' in rthread:
				subj = rthread['sub'].encode('utf-8')
			else:
				subj = 'None'
			post = util.html.format_entities(util.html.strip_tags(rthread['com'].replace('<br>',' '))).encode('utf-8')
			if len(post) > 150:
				post = post[:150] + '...'
			util.reply('http://boards.4chan.org/'+cmdtext+'/thread/'+str(rthread['no'])+' Subject: '+subj+', Post: '+post)
		except Exception, e:
			util.reply_safe('Invalid board selection.')
			print(e)