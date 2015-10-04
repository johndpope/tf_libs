#!/usr/bin/env python

""" run_test: 

Detailed description:

Notes:
    @bug:

Todo:
    @todo:

Info:
    @since: 13/09/2015
"""

import numpy as np  # Maths library
import scipy as sp  # Data analysis library
import matplotlib.pyplot as plt  # Plotting library

from scipy.optimize import curve_fit  # Curve fitting
from scipy.signal import find_peaks_cwt, argrelmax  # Peak finding
from scipy.interpolate import interp1d  # Interpolation

import os  # System directory/file operations
import shutil  # High-level file operations
import re  # Regular expressions

from pprint import pprint  # Pretty printing


from tf_debug import Debug as tfdebug
from tf_debug import demo_print

__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"

from tf_array import *
def test_tf_array():
    print('*** tf_array.py demo ***')
    print()
    x = np.linspace(0,10,101)
    y = np.linspace(10,30,101)
    l = [list(range(10))]
    l2 = [5,6,9,7,4,1,3,2,5,6]

    print("arr_range(x, var_name=False) = ", end=' ')
    print(arr_range(x, var_name=False))
    print()

    lim = [2,3.4]
    print("sub_arr(x, lim, con_array = None, min=None, max=None, boundaries=True) = ", end=' ')
    print(sub_arr(x, lim, con_array = None, min=None, max=None, boundaries=True))
    print()

    print("arr_nearest(x, 2.65467, output = 'value', side = 'both', next=0) = ", end=' ')
    print(arr_nearest(x, 2.65467, output = 'value', side = 'both', next=0))

    print(check_array(l, verbatim=1))

    print("argsort([5,6,9,7,4,1,3,2,5,6])")
    print(argsort(l2))
    print(list(l2[i] for i in argsort(l2)))

    print("\nstr_name_value(['val1','val2'], [23432.4576,34654.45764])")
    print(str_name_value(['value1','val2'], [23.4576,34654.45764]))

    return

from tf_array import *
def test_tf_const():

    return

from tf_array import *
def test_tf_data():

    return

from tf_array import *
def test_tf_deebug():

    return

from tf_array import *
def test_tf_dic():

    return

from tf_dir import *
def test_tf_dir():

    return

from tf_file import *
def test_tf_file():

    return

from tf_numeric import *
def test_tf_numeric():

    return

from tf_plot import *
def test_tf_plot():

    print('\n*** tf_plots.py demo ***\n')

    mu, sigma = 200, 25
    x = mu + sigma*np.random.randn(10000)
    # x = np.linspace(0,100)
    arr_hist((x,x*.5))
    return

from tf_string import *
def test_tf_string():

    timestamps = ['2011-06-2', '2011-08-05', '2011-02-04', '2010-1-14', '2010-12-13', '2010-1-12', '2010-2-11', '2010-2-07', '2010-12-02', '2011-11-30', '2010-11-26', '2010-11-23', '2010-11-22', '2010-11-16']
    tsort, tind = sort_dates(timestamps, format = "%Y-%m-%d", reverse = True)
    print('sort_dates(timestamps, format = "%Y-%m-%d", reverse = True)')
    print(tsort)
    print(list(timestamps[i] for i in tind))

    x = 1451.260 #4564.6548496
    err = 0.0000004894798
    print ('x =',x)

    print("strnsignif(x,nsignif=4, _verbatim=True)")
    print(strnsignif(err,nsignif=4, _verbatim=True))

    print("to_precision(1.230,4)")
    print(to_precision(1.230,4))

    print("\nstr_err(%s, %s) = " % (x, err), end='')
    print(str_err(x,err))


    return

from tf_classes import *
def test_tf_classes():
    print('\n*** tf_classes.py demo ***\n')
    I = PhysQuant('Current','I','A')
    print(I.name)

    x = np.linspace(0.5,50,100)
    param = ParamFloat(x,'I')

    Plot(title='A param plot')
    plt.gca().title('new title')


    return

if __name__ == "__main__":

    test_tf_array()
    test_tf_string()
    # test_tf_plot()
    # test_tf_classes()
