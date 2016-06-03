#!/bin/env pythdebug_ON

# Purpose: 

import numpy as np
import matplotlib.pyplot as plt     # Plotting library
import pylab
import os
import shutil
import inspect              # Line numbers etc
import sys

class debug:
    """ Debugging features """
    debug_ON = True # List of all files read so far (in order)
    plot_ON = True
    lines_ON = False
    init = False
    ndebug_ON = 0
    nOFF = 0
    lines = {}
    functidebug_ONs = {'debug_ON':[], 'off': []}

    def __init__(self, debug_ON=False, lines_ON = False, plot_ON=True):
        self.line = inspect.currentframe().f_back.f_lineno
        ## Code first time debug class is initiated
        if not debug.init:
            # print whereami(level=1)+'tf_libs <debug> instance created'#.format(self.line)
            debug.init = True
        if debug_ON:
            debug.debug_ON = True
        if lines_ON:
            debug.lines_ON = True
        if plot_ON:
            debug.plot_ON = True

    def __call__(self, *args, **kwargs):
        plot = kwargs.pop('plot', False)
        self.line = inspect.currentframe().f_back.f_lineno

        if not plot: # Normal debug print opperation
            if debug.debug_ON:
                if debug.lines_ON:
                    print module_name(level=1)+', '+line_no(level=1)+': ',
                debug_print(1, *args, **kwargs)
                debug.ndebug_ON += 1
                debug.lines[self.line] = True
            else: 
                debug.nOFF += 1
                debug.lines[self.line] = False
        else: # debug_plot
            if debug.plot_ON:
                debug_plot(*args, **kwargs) 

    def debug_ON(self):
        debug.debug_ON = True
        print 'Debugging (tf_libs): \tdebug_ON'  

    def off(self):
        debug.debug_ON = False
        print 'Debugging (tf_libs): \tOFF'

    def l(self):
        line = inspect.currentframe().f_back.f_back.f_lineno
        print '(line: {}) {}'.format(line, text)

    def count(self):
        print "line {}: {} <debug> debug_ON, {} debug OFF".format(self.line, debug.ndebug_ON, debug.nOFF)

    def info(self):
        print "line {}: {} <debug> debug_ON, {} <debug>: OFF".format(self.line, debug.ndebug_ON, debug.nOFF)
        for line, debug_ON in self.lines.iteritems():
            print ' ', line, debug_ON, ((debug_ON and ' <--') or '')
        
def get_verbose_prefix():
    """Returns an informative prefix for verbose debug output messages"""
    s = inspect.stack()
    module_name = inspect.getmodulename(s[1][1])
    func_name = s[1][3]
    return '%s->%s' % (module_name, func_name)

def func_name(level=0):
    return inspect.stack()[level+1][3]

def module_name(level=0):
    """ Return name of the module level levels from where this 
    function was called. level = 1 goes 1 level further up the stack """
    # return inspect.getmodulename(inspect.stack()[level+1][1])
    # print 'tf_debug.py, 85:', os.path.basename(inspect.stack()[level+1][1])
    try:
        name = os.path.basename(inspect.stack()[level+1][1])
    except IndexError:
        print 'tf_debug: Failed to return module name. See stack:'
        try:
            print inspect.stack()
        except:
            print "inspect module doesn't seem to be working at all!"
        name = '*UNKNOWN*'
    return name

def line_no(level=0):
    """ Return line number level levels from where this 
    function was called. level = 1 goes 1 level further up the stack """
    try:
        line = str(inspect.stack()[level+1][2])
    except IndexError:
        print 'tf_debug: Failed to return line number. See stack:'
        try:
            print inspect.stack()
        except:
            print "inspect module doesn't seem to be working at all!"
        line = '*UNKNOWN*'
    return line

def whereami(level=0):
    # string = module_name(level=level+1)+', '+func_name(level=level+1)+', '+line_no(level=level+1)+': '
    string = line_no(level=level+1)+', '+func_name(level=level+1)+', '+module_name(level=level+1)+':\t'
    return string

def debug_print( debug, *args, **kwargs ):
    """
    Purpose:
      Functidebug_ON to print informatidebug_ON about variables that can be easily
     turned debug_ON and off for debugging purposes. 
      If normal parameters are supplied, multiple variables are printed 
     to the same line, separated by tabs.
      If keyword arguments are supplied then the variables are printed 
     aldebug_ONgside the keyword names.
    
    Inputs:
     debug      bool	toggle debug mode debug_ON and off
     *args      any     variables to print
     **kwargs   any     variables to print with names
     
    Outputs: 
     (Ndebug_ONE)

    Call examples: 
     debug_print(1, var1, var2, var3)
     debug_print(debug, var1 = var1, var2 = var2, var3 = var3)
    """
    ## TODO: Use pprint.pformat
    if debug:
        if args: # If there is anything in args
            for i, arg in enumerate(args):
                if i != len(args)-1:    print ' '+str(arg)+',\t',
                else:                   print arg     
        if kwargs: # If there is anything in args
            for key, value in kwargs.iteritems():
                ## If the variable is a list that wdebug_ON't fit debug_ON debug_ONe line
                ##  start it debug_ON a new line
                ## NOTE: does not check for numpy arrays
                if (type(value) is list) and (len(value) > 6):
                    print '{} \t=\n{}'.format( key, value )
                else:
                    print '{} \t= {}'.format( key, value )

def debug_plot(*args, **kwargs):
    "Quickly plot the supplied variables"
    level = kwargs.pop('level', 0)
    xlabel = kwargs.pop('xlabel', 'x')
    ylabel = kwargs.pop('ylabel', 'y')

    # print 'debug plot on line {}'.format(line_no(level))

    if len(args) == 1: # and len(kwargs) == 0:
        x = np.arange(len(args[0]))
        y = args[0]
    elif len(args) == 2: # and len(kwargs) == 0:
        x = args[0]
        y = args[1]
    else:
        print 'WARNING: Incorrect arguements to debug_plot'
        return

    fig = plt.figure()
    fig.clear()
    ax = fig.add_subplot(1,1,1)
    plt.plot( x, y, 'k-x', **kwargs)
    plt.grid(True)
    plt.title(r"Debugging plot")#.format(iv.fn))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.legend(loc='best')


def plineno(text=False):
    """Return the current line number in the calling program."""
    line = inspect.currentframe().f_back.f_back.f_lineno
    if text:
        print '(line: {}) {}'.format(line, text)
    return line

def debug_demo():
    print '*** tf_debug.py demo ***'
    db = debug(1,1,1)

    x = np.linspace(0,10,100)
    y = np.linspace(10,30,100)
    a = [1,2,3]
    print
    print 'Line number (~181):', line_no(level=0)
    print 'Function name (debug_demo):', func_name(level=0)
    print 'Module name (tf_debug.py):', module_name(level=0)
    print file_loc_prefix(), '<Message>'
    print
    print 'debug_print tests:'
    a = 4
    arr = [4,7,3]
    str = 'hello!'
    print a, arr, str
    debug_print( 1, a, arr, str )
    debug_print( 1, a=a, arr=arr, str=str )

if __name__ == "__main__":
    debug_demo()
    pass	


