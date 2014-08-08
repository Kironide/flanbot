# utilities that help with opening and writing to files

import os, pickle

# opens a file and returns the stored object
# writes default to it if it doesn't exist
def load_file(fpath, default):
	if not os.path.exists(fpath):
		with open(fpath,'w') as f:
			pickle.dump(default,f)
	with open(fpath,'r') as f:
		return pickle.load(f)

# saves a pickled object to file
def save_file(fpath, obj):
	with open(fpath,'w') as f:
		pickle.dump(obj,f)