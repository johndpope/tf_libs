#!/usr/bin/env python

""" tf_file.py: Frequently used file operations and wrappers.

Detailed description:

Notes:
    @bug:

Todo:
    @todo: find_latest_file function using sort_dates()

Info:
    @since: 17-06-14
"""


import numpy as np
from pprint import pprint   # Pretty printing
import os
import re
# import shutil

## CAN import:    tf_debug, tf_array
## CANNOT import: tf_class
# from . import tf_numeric

__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"

def mkdir(dirs, verbatim = False):
	""" Checks if a directory exists and makes it if nessesary.
	Inputs:
		dir 			- Directory path
		verbatim = 0	- True:  print whether dir was created, 
						  False: print nothing, 
						  0:     print only if dir was created
	"""
	for dir in dirs:
		if not os.path.isdir( dir ):
			os.makedirs( dir )
			if (verbatim == 0 or verbatim):
				print('Created directory: '+dir)
		else:
			if verbatim:
				print('Directory "'+dir+'" already exists')

def fn_filter(dir, pattern, unique=False):
    """ Filenames in a given directory that match the search pattern
    TODO: add compatibility for non raw string file paths
    """
    fns = os.listdir(dir)
    p = re.compile(pattern)
    matches = []
    for fn in fns:
        if p.search(fn):
            matches.append(fn)
    if unique: # expect unique match so return scalar string that matches
        if len(matches) == 1:
            return matches[0]
        else:
            print('WARNING: fn_filter: {} matches: {}'.format(len(matches), matches))
    else:
        return matches

def ncol(fn_list, cols, dir='', filekey=False, np_arrays = False, header_len = 0, debug = False):
	"""
	set filekey = True to nest data inside dictionary keyed to filenames
	"""
	# cols should be a dictionary of col#:'variable_name' pairs
	# The returned dictionary has the variable_names as keys associated 
	# with the data in that column

	if isinstance(fn_list, str):	# make fn_list a list if it isn't already
		fn_list =[fn_list]
		if debug:
			print('tf_file: Filename string converted to list: ', fn_list)

	#data = {array([])} if np_arrays==True else {[]}
	
	# Initialise dictionary to hold data from all required files
	fn_data = {}

	for fn in fn_list:
		if debug:
			print('tf_file: Reading file: '+dir+fn)
		# Create a dictionary of arrays to hold the data from each column of one file
		data = {}
		bad_lines = [] # Record of line number that were not read correctly
		for name in list(cols.values()):
			data[name] = [] 

		for (i, line) in enumerate(open( dir+fn,'rb' )):
			if debug == 10: print('tf_file: line {}: '.format(i+1), line.rstrip('\n')) # don't print newline char

			if i <= header_len-1:	# Skip column headings etc
				continue

			values = line.split()#.strip()

			for i, val in enumerate(values): # Convert numeric values to floats
				values[i] = float(val) if tf_numeric.is_number(val) else val
			
			try:
				for col_no, name in cols.items(): 
					data[name].append(values[col_no-1]) 
			except IndexError:
				print('Not enough columns on line {}? of file: {}'.format( i+1, fn )) # Seems to always print line number as 1?	
				bad_lines.append(i)
				if debug:
					print('tf_file: line {}: '.format(i+1), line.rstrip('\n'))
					print('tf_file: values: ', values)
			continue

		# Associate data from file with the filename
		fn_data[fn] = data

	if bad_lines != []:
		print('tf_file: Line numbers not read correctly: ', bad_lines)
	# print data
	# print fn_data
	# print
	# pprint.pprint(fn_data)

	#| If only given one filename and filekey == False do not nest data in filenames dictionary
	if len(fn_list)==1 and filekey == False: 
		if debug: print('tf_file: returned data without filename nesting (filekey == 0)')
		return data
	else: 
		if debug: print('tf_file: returned data with filename nesting')
		return fn_data


def find_latest_file(file_names):
	""" Return filename containing most recent date	"""

	return

def main():
	fn = ['chi_im_tot']
	data = ncol(fn, {2:'q', 8:'chi'})
	print(data)
	pass
	

if __name__ == "__main__":
    main()
