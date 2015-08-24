#!/bin/env python

#==============================================================================
# Purpose: 
#
# Description:
#  
# Notes:
#  
# Reminders:
#
# Author:   Tom Farley
# Created:  00-00-14
# Modified: 00-00-14  
#==============================================================================

from itertools import repeat

def str_err(value, error, nsf = 1, latex=False, separate=False):
	""" Given a value and error, finds the position of the first sifnificant 
		digit of the error and returns a string contianing both value and
		error to the same number of sifnificant digits separated by a +/-
		Inputs:
			value 		value to be rounded
			error 		error to determine rounding
			nsf			number significant figures
			latex		use latex \pm symbol
			separated 	return separate value and error strings (over-rides '\latex')
	"""
	from numpy import floor, log10, sign
	## REMEMBER: Look at IDL routine for how to extend!
	## NOTE: Pass keywords by reference doesn't work for value_str=value_str, err_str=err_str
	## TODO: implement
	# In [79]: '{:.{s}f}'.format(1.234, s = 2)
	# Out[# 79]: '1.23'

	## Default format code when error cannot be used to determine sig figs
	fmt_dflt = ':0.3g'

	## Check input is sensible
	if error < 0:
		print "WARNING: error passed to str_err is -ve"
		fmt_str = '{'+fmt_dflt+'} +/- (-ve err!)'
		return fmt_str.format(value)
	elif error == 0:
		print "WARNING: error passed to str_err is 0.0"
		fmt_str = '{'+fmt_dflt+'} +/- 0.0 (!)'
		return fmt_str.format(value)

	## Find first significant figure of error
	if error < 1.0:

		## Put number of significant digits to display into a string
		sf_err = abs(floor(log10(error)))
		try:
			sf_str = str(int(sf_err))
		except OverflowError as detail:
			## err is probably floating infinity
			return '{} +/- inf ({})'.format(value, detail)

		## Create separate value and error strings
		format_string = r"{:0."+sf_str+"f}"
		value_str 	= format_string.format(value)
		err_str 	= format_string.format(error)

		## Return keyword depended output format
		if   (latex == True)  and (separate == False):  # Return single string contianing \pm
			comb_str = value_str + r" $\pm$ " + err_str
			return comb_str
		elif (latex == False) and (separate == False):  # Return single string contianing +/-
			comb_str = value_str + r" +/- " + err_str
			return comb_str
		elif (separate == True): 	# Return value and error in separate strings
			return value_str, err_str

	elif error >= 1.0:
		## NEED  TO FIX CASE WHERE ERROR IS BIGGER THAN VALUE!


		## Put number of significant digits to display into a string
		# sign_value = sign(value)
		sf_err = floor(log10(error))+1
		sf_value = floor(log10(abs(value)))+1
		try:
			sf_str = str(int(sf_err))
		except OverflowError as detail:
			## err is probably floating infinity
			return '{} +/- inf ({})'.format(value, detail)

		## Create separate value and error strings
		format_string = r"{:0.0f}"
		value_str 	= format_string.format(round(value*10**-(sf_value-sf_err))*10**(sf_value-sf_err))
		err_str 	= format_string.format(round(error*10**-(sf_err-1))*10**(sf_err-1))

		## Return keyword depended output format
		if   (latex == True)  and (separate == False):  # Return single string contianing \pm
			comb_str = value_str + r" $\pm$ " + err_str
			return comb_str
		elif (latex == False) and (separate == False):  # Return single string contianing +/-
			comb_str = value_str + r" +/- " + err_str
			return comb_str
		elif (separate == True): 	# Return value and error in separate strings
			return value_str, err_str
	else: 
		return "(str_err cannot handel this value-error combination yet)"
		
			
			# if latex == True:
			# 	format_string = r"{:0."+sf_str+"f} $\pm$ {:0."+sf_str+"f}"
			# 	str_err = format_string.format(value, error)
			# else: 
			# 	format_string =  "{:0."+sf_str+"f} +/- {:0."+sf_str+"f}"
			# 	str_err = format_string.format(value, error)


def str_popt(popt, pcov, check=[0,1,2], strings=None, 
			units = None, latex=False):
	""" Print fit parameters from sciipy.curvefit 

	"""
	if units == None:
		units = list(repeat('', len(check)))
	if strings == None:
		strings = ['popt['+str(i)+']' for i in check]
	nl = list(repeat('\n', len(check)-1)) + ['']
	string = ''
	for i in check:
		dprint(1, i=i)
		#print strings, popt, units, nl
		string += (strings[i] + '\t = ' + str_err(popt[i], sqrt(pcov[i][i]), latex=latex) + ' ' + 
			units[i] + nl[i])
	return string

def scs(str1, str2=False, append = False, separator='/'):
    """ String character separator: 
    -If only str1 is supplied, appends a separator (default:'/') to the string 
    if not already pressent.  
    -If both str1 and str2 supplied, the two strings are concatenated such that 
    they are separated by one separator characher (default:'/')
    *If append is true only the second argement (str2) is returned w or w/o the
    required separator """
    # print str1, str2
    if str2: # combine two path strings
        ## Do not add or remove any separators if one string is empty - ideally remove separators at join...
        if (str1 == '') or (str2 == ''): ## NOTE: This may not work properly in str_comb! ******
            return str1+str2
        end = str1.endswith(separator)      # True if ends in '/'
        start = str2.startswith(separator)  # True if starts with '/'
        if (not end) and (not start): # add slash between path elements
            if append: return separator+str2
            else:      return str1+separator+str2
        elif end and start: # remove slash between path elements
            if append: return str2[1:]
            else:      return str1+str2[1:]
        else: # Either begining or end already has a slash
            if append: return str2
            else:      return str1+str2

    else: # check end of one string
        if ~str1.endswith(separator):
            return str1+separator
        else:
            return str1
        
def comb_str(*args, **kwargs):
    """ Combine strings into one string, each element separated by separator character (dflt:'/') """
    separator = kwargs.pop("separator", '/')
    comb_str = args[0]
    for str1, str2 in zip(args, args[1:]): # create tuples of adjacent strings
        comb_str += scs(str1, str2=str2, append=True, separator=separator)            
    return comb_str

def test_print():
	print "Here is a string"

if __name__ == "__main__":
    print '*** tf_string.py demo ***'
    x = linspace(0,10,100)
    y = linspace(10,30,100)

    a = [1,2,3]
    str_popt(a,a)


    pass
