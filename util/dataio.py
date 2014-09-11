# utilities that help with opening and writing to files

import os, pickle

# opens a file and returns the stored object
# writes default to it if it doesn't exist
def load_file(fpath, default):
	if not os.path.exists(fpath):
		with open(fpath,'wb') as f:
			pickle.dump(default,f)
	with open(fpath,'rb') as f:
		return pickle.load(f)

# saves a pickled object to file
def save_file(fpath, obj):
	with open(fpath,'wb') as f:
		pickle.dump(obj,f)

# opens a file and reads the raw contents
# returns None if path does not exist
def load_raw(fpath):
	if not os.path.exists(fpath):
		return None
	with open(fpath,'rb') as f:
		temp = f.read()
	return temp

# saves some raw data to file
def save_raw(fpath, data):
	with open(fpath,'wb') as f:
		f.write(data)