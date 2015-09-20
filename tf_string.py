#!/usr/bin/env python

""" tf_string.py: Frequently used string operations and wrappers.

Detailed description:

Notes:
    @bug:

Todo:
    @todo: Use to_precision
    @todo: Extend strnsignif to arrays of values

Info:
    @since: 18/09/2015
"""

from itertools import repeat
import datetime
import numpy as np
import math
import tf_array
from tf_debug import debug

__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"

db = debug(debug_ON=0, lines_ON = False, plot_ON=False)

def to_precision(x,p):
    """ Return a string representation of x formatted with a precision of p

    strnsignif also adds trailing 0s for correnct # of sf to functionality is same

    From: http://randlet.com/blog/python-significant-figures-format/
    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """

    x = float(x)

    if x == 0.:
        return "0." + "0"*(p-1)

    out = []

    if x < 0:
        out.append("-")
        x = -x

    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)

    if n < math.pow(10, p - 1):
        e = e -1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)

    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1

    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1

    m = "%.*g" % (p, n)

    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (p -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)
    return "".join(out)

def _char_before_dp(x):
    """ digits before decimal point """
    x = np.abs(x)
    n = int(np.floor(np.log10(x)))
    if x >= 1:
        return n+1
    elif x < 1:
        return 0

def _lead_zeros_after_dp(x):
    """ Number of zero characters after dp and before 1st sf """
    x = np.abs(x)
    n = int(np.floor(np.log10(x)))
    db(n=n)
    if x < 1:
        return abs(n+1)
    elif x >= 1:
        return 0

def strnsignif(x, nsignif=3, scientific=False, _verbatim=False):
    """ Return string format of number to supplied no. of significant figures
    Ideas from: http://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
    Note: Does not round up for: strnsignif(-55.55,nsignif=3 ==> -55.5  -- Not sure why...?"""
    assert nsignif >= 1, 'Negative number of significant figures supplied'
    nsignif = int(nsignif)

    if _verbatim: print('_before_dp: ',_char_before_dp(x))

    ## %g rounds, but will give scientific e-7 etc notation, so use %f to get all places
    ## %s sometimes uses scientific notation, so use %f instead, however always gives 6 dp precision
    format_str = '%.'+str(nsignif)+'g'
    strn = '%f' % float(format_str % x)
    ## %s always formats with a decimal point ie .0

    ## Remove -ve sign and add it at the end to simplify counting no of characters in string
    if x<0: strn = strn[1:]

    ## Add trailing 0s of precision if they are missing (only used for %s above, not %f)
    if (len(strn)-1) < nsignif:
        strn += '0'*(nsignif-(len(strn)-1))
    ## Remove false trailing .0 giving false impression of precission
    elif _char_before_dp(x) >= nsignif: # again important if %s used above
        strn = strn.split(sep='.')[0]

    ## %f always gives at least 6dp of precision therefore remove false zeros
    if '.' in strn:
        char_after_dp = len(strn.split(sep='.')[1])

        db(strn=strn)
        db(_char_before_dp=_char_before_dp(x))
        db(char_after_dp=char_after_dp)
        db(_lead_zeros_after_dp=_lead_zeros_after_dp(x))

        extra_zeros = _char_before_dp(x)+char_after_dp - _lead_zeros_after_dp(x) - nsignif
        # assert extra_zeros >= - _lead_zeros_after_dp(x) 'Displaying too few significant figures...!'

        if extra_zeros==0:
            ## Can't find way to numerically index final element in range equiv to [0:]
            strn = strn.split(sep='.')[0]+'.'+ strn.split(sep='.')[1][0:]
        elif extra_zeros > 0:
            strn = strn.split(sep='.')[0]+'.'+ strn.split(sep='.')[1][0:-1-(extra_zeros-1)]

    ## Add -ve sign if removed
    if x<0: strn = '-'+strn

    return strn


def str_err(value, error, nsf = 1, latex=False, separate=False):
    """ Given a value and error, finds the position of the first sifnificant
        digit of the error and returns a string contianing both value and
        error to the same number of sifnificant digits separated by a +/-
        Inputs:
        c      value 		value to be rounded
            error 		error to determine rounding
            nsf			number significant figures
            latex		use latex \pm symbol
            separated 	return separate value and error strings (overrides '\latex')
    """

    ## Check for sensible inputs
    assert error > 0, "str_err received negative error"
    assert not (error == 0), "str_err received zero valued error"
    assert nsf >= 1, "str_err received nsf less than 1"

    ## Find number of additional digits needed in value than error assuming 1sf required
    nsf_val = np.floor(np.log10(abs(value))) - np.floor(np.log10(error))

    ## Add additional sf as requested
    nsf_val += (nsf)

    ## If last required sf in error is at least an order of magnitude greater than the error display
    ## no additional digits (not negative additional digits)
    if nsf_val < 0: nsf_val = 0

    db(nsf_val=nsf_val)

    value_str = strnsignif(value, nsf_val)
    err_str = strnsignif(error, nsf)

    ## Return keyword depended output format
    if   (latex == True)  and (separate == False):  # Return single string contianing \pm
        comb_str = value_str + r" $\pm$ " + err_str
        return comb_str
    elif (latex == False) and (separate == False):  # Return single string contianing +/-
        comb_str = value_str + r" +/- " + err_str
        return comb_str
    elif (separate == True): 	# Return value and error in separate strings
        return value_str, err_str



def str_err_old(value, error, nsf = 1, latex=False, separate=False):
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

	## Check input is sensible - could use assert
	if error < 0:
		print("WARNING: error passed to str_err is -ve")
		fmt_str = '{'+fmt_dflt+'} +/- (-ve err!)'
		return fmt_str.format(value)
	elif error == 0:
		print("WARNING: error passed to str_err is 0.0")
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
		print("i=",i)
		#print strings, popt, units, nl
		string += (strings[i] + '\t = ' + str_err(popt[i], np.sqrt(pcov[i][i]), latex=latex) + ' ' +
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



def sort_dates(dates_in, format = "%Y-%m-%d", reverse = True):
    """Sort dates chronologically
    Note: This will add padded zeros if they are nor already present therefore output not always equal to input
    basic method from: http://stackoverflow.com/questions/5166842/sort-dates-in-python-array """
    dates = [datetime.datetime.strptime(d, format) for d in dates_in]
    indices = tf_array.argsort(dates, reverse=reverse)
    dates.sort(reverse = reverse)
    sorted = [datetime.datetime.strftime(d, format) for d in dates]
    return sorted, indices

def test_print():
	print("Here is a string")

if __name__ == "__main__":
    print('*** tf_string.py demo ***')
    x = np.linspace(0,10,100)
    y = np.linspace(10,30,100)

    a = [1,2,3]
    str_popt(a,a)


    pass
