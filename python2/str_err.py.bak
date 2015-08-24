


## OLD, now in tf_str *********************************************************************************************


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
	from numpy import floor, log10
	## REMEMBER: Look at IDL routine for how to extend!
	## NOTE: Pass keywords by reference doesn't work for value_str=value_str, err_str=err_str

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
	else: 
		return "(str_err cannot handel this value-error combination yet)"
		
			
			# if latex == True:
			# 	format_string = r"{:0."+sf_str+"f} $\pm$ {:0."+sf_str+"f}"
			# 	str_err = format_string.format(value, error)
			# else: 
			# 	format_string =  "{:0."+sf_str+"f} +/- {:0."+sf_str+"f}"
			# 	str_err = format_string.format(value, error)
