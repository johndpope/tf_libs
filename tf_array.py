#!/usr/bin/env python

""" tf_array.py: Frequently used array operations and wrappers.

Keyword arguments:
    newarg -- type, description (default 0.0)
    newarg -- type, description (default 0.0)

Detailed description:

Notes:
    @bug:

Todo:
    @todo: sub_arr(arr, between=[start, end]) using extract

Info:
    @since: 17-06-14
"""

import numpy as np                  # Maths library
import matplotlib.pyplot as plt     # Plotting library

from scipy.optimize import curve_fit                # Curve fitting
from scipy.signal import find_peaks_cwt, argrelmax  # Peak finding
from scipy.interpolate import interp1d              # Interpolation

import os           # System directory/file opperations
import shutil       # High-level file operations
import re           # Regular expressions

from pprint import pprint   # Pretty printing

from tf_debug import debug_print as dprint

# debug = 0
# plot = 1

def sub_arr(array, lim, con_array = None, min=None, max=None, boundaries=True):
    """Purpose: Extract sub array of values between min and max limits
    arguements:
     array          var     array to take subset of
     lim            var     array containing [min, max]
    keywords:
     con_array      var     condition array to apply min/max check on
    Outputs:
     array of values in array with indices satisfying min < con_array < max
    Call example: 
     function()

     TODO: Update to convert normal lists to numpy arrays
    """
    if con_array == None:
        con_array = array
    else: 
        if np.size(con_array) != np.size(array):
            print('WARNING: size(con_array) != size(array)')
    if boundaries == True:
        sub = np.extract( (con_array>=lim[0]) * (con_array<=lim[1]), array)
    else:
        sub = np.extract( (con_array>lim[0]) * (con_array<lim[1]), array)
    return sub

def extract_2D(arr1, arr2, condition):
    """ Return elements of two arrays where indices match condition """
    inds = np.nonzero(condition)
    return arr1[inds], arr2[inds]

def arr_range(array, var_name=False):
    """ Return numeric range of array as two element array """
    range = np.array([min(array), max(array)])
    if var_name:
        print(var_name, 'range:', range)
    return range

def arr_nearest(array, value, output = 'value', side = 'both', next=0):
    """Element in nd array closest to the scalar value
    Use 'next' to return next nearest values"""
    if side == 'both':
        idx = np.abs(array - value).argmin()
    elif side =='above':
        idx = (array - value)
        idx = np.abs(np.extract(idx>0, idx)).argmin()
    elif side == 'below':
        idx = (array - value)
        idx = np.abs(np.extract(idx<0, idx)).argmin()
    else:
        print('arr_nearest: Invalid side anguement')

    if (output == 'value') or (output == 'v'):
        return array.flat[idx]
    elif (output == 'index') or (output == 'i'):
        return idx
    else:
        print('arr_nearest: Invalid output arguement:', output)
        print("\t Accepted arguments: 'value', 'v', 'index', 'i'")

def closest_max(x, y, x0, order = 3, output = 'value'):
    """ x value/index of max y value closest to x0 
    Requires arr_nearest 
    """
    imax = argrelmax(y, order = order)[0] # Extract maximum in dI
    i0 = arr_nearest(x, x0, output='index')
    iclose =  arr_nearest(imax, i0, output='value')
    x1 = imax
    
    if (output == 'value') or (output == 'v'):
        return x[iclose]
    elif (output == 'index') or (output == 'i'):
        return iclose
    else:
        print('arr_nearest: Invalid output arguement:', output)
        print("\t Accepted arguments: 'value', 'v', 'index', 'i'")

def is_scalar(var):
    """ True if variable is scalar """
    if hasattr(var, "__len__"):
        return False
    else:
        return True

def safe_len(var):
    """ Length of variable returning 1 instead of type error for scalars """
    if np.isnan(var):
        return 0
    elif tf.is_scalar(var): # checks if has atribute __len__
        return 1
    else:
        return len(var)

def function(required_arg, *args, **kwargs):
    """ 
    Inputs:
     *args          var     purpose
     **kwargs       dict    purpose     
    Outputs:
     
    Call example: 
     
    """

    dprint(debug, required_arg)

    ## args will be a list of positional arguments
    ## because it has * before it
    if args: # If there is anything in args
        print(args)

    ## kwargs will be a dictionary of keyword arguments,
    ## because it has ** before it
    if kwargs: # If there is anything in kwargs
        print(kwargs)

    x = linspace(0,10,100)
    y = linspace(0,10,100)
    
    ## Plot results
    plt.plot( x[:], y[:], '-o', label ='')
    
    ## Format plot
    plt.grid(True)
    plt.title(r"$\Delta")
    plt.xlabel("")
    plt.ylabel("")
    plt.legend(loc='best')
    ## Display transparrent legend, with round corners
    legend = plt.legend(loc='upper right', fancybox=True)
    legend.get_frame().set_alpha(0.5)
    
    if plot: plt.show() # Display plot if: plot=True

    return


if __name__ == "__main__":
    print('*** tf_array.py demo ***')
    print()
    x = np.linspace(0,10,101)
    y = np.linspace(10,30,101)
    
    print("arr_range(x, var_name=False) = ", end=' ')
    print(arr_range(x, var_name=False))
    print()

    lim = [2,3.4]
    print("sub_arr(x, lim, con_array = None, min=None, max=None, boundaries=True) = ", end=' ')
    print(sub_arr(x, lim, con_array = None, min=None, max=None, boundaries=True))
    print()

    print("arr_nearest(x, 2.65467, output = 'value', side = 'both', next=0) = ", end=' ')
    print(arr_nearest(x, 2.65467, output = 'value', side = 'both', next=0))
    pass

