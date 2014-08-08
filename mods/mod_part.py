import util

def main(cmdtext):
	if cmdtext == '':
		if util.c_target.startswith('#'):
			util.partchan(util.c_target)
	else:
		util.partchan(cmdtext.split(' ')[0])