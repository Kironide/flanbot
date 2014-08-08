# miscellaneous
import random, os, imp, multiprocessing, itertools
import settings
from pyxdameraulevenshtein import damerau_levenshtein_distance as distance
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance as norm_distance

# prints info about exceptions
def handle_exception(e):
	print(e)

# given list, returns dict of item -> list of all permutations of item
def perm_dict(items):
	perm = {}
	for item in items:
		perm[item] = [''.join(p) for p in itertools.permutations(item)]
	return perm

# a random thing to append to the end of messages
def randext():
	return settings.responses[random.randint(1,len(settings.responses))-1]

# returns a list of dynamically called modules
def cmds_normal():
	return [x.replace('.py','')[len(settings.prefix_mods):] for x in os.listdir(settings.folder_mods+'/') if x.endswith('.py') and x.startswith(settings.prefix_mods)]

# returns a list of all mods
def cmds_all():
	temp = cmds_normal()
	temp.append('reload')
	return sorted(temp)

# returns a list of all events
def events_all():
	return [x.replace('.py','')[len(settings.prefix_events):] for x in os.listdir(settings.folder_events+'/') if x.endswith('.py') and x.startswith(settings.prefix_events)]

# returns a list of all utility modules in form util.mod
def utils_all():
	return ['util.'+x.replace('.py','') for x in os.listdir('util/') if x.endswith('.py') and x != '__init__.py']

# returns a list of all books
def books_all():
	return [x.replace('.txt','') for x in os.listdir(settings.folder_books+'/') if x.endswith('.txt')]

# execute command
def exec_cmd(modname,inputstr,folder):
	pref = ''
	if folder == settings.folder_mods:
		pref = settings.prefix_mods
	elif folder == settings.folder_events:
		pref = settings.prefix_events
	path = folder+'/'+pref+modname+'.py'
	# print('Loading module from: '+path) # this prints a lot
	mod = imp.load_source(modname,path)
	if modname in ['server','quit']:
		mod.main(inputstr)
	else:
		p = multiprocessing.Process(target=mod.main,args=(inputstr,))
		p.start()
		p.join()

# attempts to match some malformed input against a list of potentially correct inputst
# returns (guess, supplement) where supplement is a potentially incorrectly appended substring of the malformed input
# returns None to indicate no unique maches found
def match_input(input_wrong, correct):
	valid = []
	supplement = ''
	perm = {}

	# checks if a valid command is a substring of input
	for input_correct in correct:
		if input_correct in input_wrong:
			valid.append(input_correct)

	# if one is found, then check if input begins with input_wrong
	# if so, user probably did an accidental concatenation
	if len(valid) == 1:
		if input_wrong.startswith(valid[0]):
			supplement = input_wrong[len(valid[0]):]

	# checks if D-L distance is 1
	if len(valid) == 0:
		for input_correct in correct:
			if distance(input_wrong,input_correct) == 1:
				valid.append(input_correct)

	# checks if D-L distance is 2 or norm. D-L distance <= 3
	if len(valid) == 0:
		for input_correct in correct:
			if distance(input_wrong,input_correct) == 2 or norm_distance(input_wrong,input_correct) <= 0.3:
				valid.append(input_correct)

	# checks if a permutation of a valid command is a substring of input
	if len(valid) == 0:
		perm = perm_dict(correct)
		for input_correct in correct:
			for p in perm[input_correct]:
				if p in input_wrong and input_correct not in valid:
					valid.append(input_correct)

	# checks if a unique valid command starts with the input
	if len(valid) == 0:
		for input_correct in correct:
			if input_correct.startswith(input_wrong):
				valid.append(input_correct)

	# check if commands starts with substrings of input
	# probably should be a last resort measure
	substr_len = 1
	while len(valid) == 0 and substr_len <= len(input_wrong):
		substr_input_wrong = input_wrong[:substr_len]
		for input_correct in correct:
			if input_correct.startswith(substr_input_wrong):
				valid.append(input_correct)
		substr_len += 1

	# checks if D-L distance is 3
	if len(valid) == 0:
		for input_correct in correct:
			if distance(input_wrong,input_correct) == 3:
				valid.append(input_correct)

	# checks if there is a permutation with D-L distance of 1
	if len(valid) == 0:
		for input_correct in correct:
			for p in perm[input_correct]:
				if distance(p,input_wrong) == 1 and input_correct not in valid:
					valid.append(input_correct)

	# if there are multiple valid commands found, choose the one that starts
	# with same letter as input (if unique)
	if len(valid) > 1:
		to_remove = []
		for input_wrong_temp in valid:
			if input_wrong_temp[0] != input_wrong[0]:
				to_remove.append(input_wrong_temp)
		for input_wrong_temp in to_remove:
			valid.remove(input_wrong_temp)

	if len(valid) == 1:
		return valid[0],supplement
	return None

# just matches using D-L
# returns a match or None
# also ignores capitalization
def match_input_weak(input_wrong, correct):
	valid = []
	if len(valid) == 0:
		for input_correct in correct:
			if distance(input_wrong.lower(),input_correct.lower()) == 1:
				valid.append(input_correct)
	if len(valid) == 0:
		for input_correct in correct:
			if distance(input_wrong.lower(),input_correct.lower()) == 2:
				valid.append(input_correct)
	if len(valid) == 0:
		for input_correct in correct:
			if distance(input_wrong.lower(),input_correct.lower()) == 3:
				valid.append(input_correct)
	if len(valid) == 0:
		for input_correct in correct:
			if distance(input_wrong.lower(),input_correct.lower()) == 4:
				valid.append(input_correct)
	if len(valid) == 1:
		return valid[0]
	return None