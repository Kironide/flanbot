import util

def main(cmdtext):
	if cmdtext == '':
		if util.cparser.target_is_channel():
			util.partchan(util.current_target())
	else:
		util.partchan(cmdtext.split(' ')[0])