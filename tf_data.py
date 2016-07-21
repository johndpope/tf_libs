#!/usr/bin/env python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

""" tmp.py: Frequently used data processing operations and wrappers.

Detailed description:

Notes:
    @bug:

Todo:
    @todo:

Info:
    @since: 18/09/2015
"""

import numpy as np                  # Maths library
import matplotlib.pyplot as plt     # Plotting library

# from scipy.optimize import curve_fit                # Curve fitting
from scipy.signal import find_peaks_cwt, argrelmax  # Peak finding
# from scipy.signal import savgol_filter              # Smoothing
from scipy.interpolate import interp1d              # Interpolation

from pprint import pprint   # Pretty printing

## CAN import:    tf_debug, tf_array
## CANNOT import: tf_class
# from tf_libs.tf_debug import debug_print as dprint

import tf_libs.tf_debug as tf_debug

db = tf_debug.Debug(0,1,1)

__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"

def interp_val(x, y, x0, kind='linear'):
    "Interpolated y value at x0 (scipy.interpolate.interp1d wrapper)"
    ## TODO: add numpy array check
    x = np.array(x)
    y = np.array(y)
    isort = np.argsort(x) # interp x values must be monotonically increasing
    finterp = interp1d(x[isort], y[isort], kind=kind) # cubic noisy
    y0 = finterp(x0)#[0] #???
    return y0

def central_diff(x, y, n=1):
    """ Calculate central difference derivate """
    ## Cannot calc central derivative of first element
    diffs = np.array([float('NaN')])
    for i in 1+np.arange(len(x)-2):
        if x[i+1] == x[i-1]: # dx=0
            dydx = float('Inf')
        else:
            dydx = (y[i+1] - y[i-1]) / (x[i+1]-x[i-1])
        diffs = np.append(diffs, dydx)
    ## Cannot calc central derivative of last element    
    diffs = np.append(diffs, float('NaN'))

    ## Calculate higher derivatives recursively - are the NaNs ok?
    if n>1:
        n -= 1
        diffs = central_diff(x, diffs, n=n)

    return diffs    

def argrelmax_global(array):
    """ Inedex of glabal array maximum """
    order = len(array)
    imax = argrelmax(array, order = order)[0]
    if len(imax)==0:
        # print "WARNING: argrelmax_gloabal failed to find a global maximum - trying orders < {}".format(order)
        print("WARNING: argrelmax_gloabal failed to find a global maximum - using max/where".format(order))
        ## I think this happens when two or more max points have the same value - common in low res data 
    else:
        return imax
    
    maximum = np.amax(array)
    imax = np.nonzero(array==maximum)[0]
    print('imax = {}, from max/where method, max = {}'.format(imax[0], maximum))

    # while len(imax) == 0:
    #     try:
    #         order -= 1
    #         imax = argrelmax(array, order = order)[0] # Extract index of global maximum 
    #     except IndexError:
    #         raise
    # print 'imax = {}, for order = {}'.format(imax, order)

    return imax[0]
            
def conv_diff(y_data, width=51, order=1):
    """ Normalised derivative of data convolved with gaussian """
    
    x1 = np.linspace(-3,3,width) # +/- 3 sigma of gaussian, sampled at width # of points
    gauss0 = np.exp(-x1**2)
    gauss1 = (-2*x1) * np.exp(-x1**2)
    gauss2 = (4*x1**2) * np.exp(-x1**2) 
    gauss3 = (-8*x1**3) * np.exp(-x1**2)
    gauss4 = (32*x1**4) * np.exp(-x1**2)

    # if order == 0:
    #     y1 = gauss0
    # elif order == 1:
    #     y1 = gauss1
    # elif order == 2:
    #     y1 = gauss2
    # elif order == 3:
    #     y1 = gauss3
    # elif order == 3:
    #     y1 = gauss4
    # else:
    #     raise RuntimeError('conv_diff got unexpected order arguement value')

    if order>0:
        y1 = gauss1

        y_conv = np.r_[y_data[width-1:0:-1],y_data,y_data[-1:-width:-1]] # mirror data at edges
        y_conv = np.convolve(y_conv, y1, mode="same")
        y_conv = y_conv[(width-1):-(width-1)] # "-(width-1)" is slight bodge to get right number of elements
        y_conv /= np.amax(np.absolute(y_conv)) # normalise output (not rigourus!)

        y_conv = conv_diff(y_conv, width=width, order=order-1)

        return y_conv
    else: return y_data


def find_linear(x_data, y_data, width=51, gap_length=3, data_length=10, 
                tol_type='rel_peak', tol=0.6, plot=False, fig_name=False):
    """ Identify linear sections in experimental data 
    x_data, y_data - experimental data
    width - convolution smoothing width
    Returns two lists of arrays containing x data and y data for each linear section
    """
    ## Approach 1:
    # create convolution kernel for calculating the smoothed second order derivative from:
    # http://stackoverflow.com/questions/13691775/python-pinpointing-the-linear-part-of-a-slope
    x1 = np.linspace(-3,3,width) # +/- 3 sigma of gaussian, sampled at width # of points

    ## Try normalising this gaussian?

    # db(x1=len(x1))
    norm = np.sum(np.exp(-x1**2)) * (x1[1]-x1[0]) # ad hoc normalization
    ## Twice differentiated normal distribution - not sure about -2 and norm
    y1 = (4*x1**2 - 2) * np.exp(-x1**2) / width *8#norm*(x1[1]-x1[0])
    y2 = (-8*x1**3) * np.exp(-x1**2) / width *8 # for third derivative

    ## Add mirroed data at ends
    # db(len(y_data[width-1:0:-1]), len(y_data[-1:-width:-1]))
    y_conv = np.r_[y_data[width-1:0:-1],y_data,y_data[-1:-width:-1]]
    y_conv2 = np.r_[y_data[width-1:0:-1],y_data,y_data[-1:-width:-1]]
    ## Calculate second order deriv. through convolution
    y_conv = np.convolve(y_conv, y1, mode="same")
    y_conv2 = np.convolve(y_conv2, y2, mode="same")
    # db( len(y_conv[0:(width-1)]), len(y_conv[-(width):-1]) )
    ## Remove mirrored data at ends
    y_conv = y_conv[(width-1):-(width-1)] # "-(width-1)" is slight bodge to get right number of elements
    y_conv2 = y_conv2[(width-1):-(width-1)] # "-(width-1)" is slight bodge to get right number of elements
    
    ## Approach 2:
    ## Use home made central diff applied to smoothed fit
    y_smooth = smooth(y_data, window_len=58, window='hamming')
    y_cent = central_diff(x_data, y_smooth, n=2)
    # y_cent *=  np.amax(y_conv) / np.amax(y_cent) # smooth(y_cent, window_len=10)

    # db(len(y_data), len(y_conv), len(y_smooth), len(y_cent))
    # db(y_conv=y_conv)

    ## Find where 2nd derviative goes above tollerance
    if tol_type=='abs':
        tol = tol # tol = 1.8e-7
    elif tol_type=='rel_peak':
        ## Tolerance in 2nd derviative taken relative to maximum in 2nd derivative
        tol = tol * np.amax(y_conv)
    elif tol_type=='rel_mean':
        tol = tol * np.average(np.absolute(y_conv))

    lims = interp_val(y_conv, x_data, tol)
    #db(lims=lims)
    x_intol, y_intol = tf.extract_2D(x_data, y_data, np.abs(y_conv)<=tol)
    
    xlinear, ylinear = data_split(x_intol, y_intol, gap_length=gap_length, data_length=data_length)
    
    # db('{} linear region(s) identified'.format(len(xlinear)))

    if plot:
        # plot data
        fig = plt.figure(fig_name) if fig_name else plt.figure() 
        fig.clear()
        ## Plot data
        plt.plot(x_data, y_data,"o", label = "noisy data")
        plt.plot(x_data, y_smooth,"x-", label = "smoothed data")
        for x, y in zip(xlinear, ylinear):
            plt.plot(x, y, "or", label = "linear data")
            plt.axvline(x[0], linestyle = '--', color ='k', alpha=0.5)
            plt.axvline(x[-1], linestyle = '--', color ='k', alpha=0.5)
        ## Plot 2nd derivative (shitfted to data)
        shift = np.average(y_data)
        plt.plot(x_data, y_conv+shift, '-', label = "conv second deriv", alpha=0.6)
        plt.plot(x_data, y_conv2, '-', label = "conv third deriv", alpha=0.6)
        plt.plot(x_data, y_cent+shift, '--', label = "central second deriv", alpha=0.6, color=(0.7,0.2,0.5))
        # plt.axhline(0)
        plt.axhline(0+shift, linestyle = '--', color ='k', alpha=0.5)
        # plt.axhline(tol)
        # plt.axvspan(0,4, color="y", alpha=0.2)
        # plt.axvspan(6,14, color="y", alpha=0.2)
        plt.axhspan(-tol+shift,tol+shift, color="b", alpha=0.4)
        # plt.vlines([0, 4, 6],-10, 10)
        # plt.xlim(-2.5,12)
        # plt.ylim(-2.5,6)
        plt.legend(loc='best')
        plt.show()
    
    return xlinear, ylinear

def data_split(x, y, gap_length=3, data_length=10, verbose=True):
    "Split data at gaps"
    i = np.arange(len(x))
    ## Find the average distace between the x data
    diff = np.diff(x)               # differences between adjacent data
    av_gap = np.average(diff)       # average separation
    ## Get indices of begining of gaps sufficiently greater than the average
    igap = np.nonzero(diff>gap_length*av_gap)[0] # nonzero nested in tuple
    
    if verbose: print('data_split: {} gap(s) identified: {}'.format(len(igap), igap))

    xsplit = []
    ysplit = []
    isplit_all = []
    ## No gap => 1 linear section, 1 gap => 2 linear sections, 2 pags => 3 linear sections etc.
    ## If no gaps, don't split the data
    if len(igap) == 0:
        xsplit.append(x)
        ysplit.append(y)
        isplit_all.append(i)
    else:
        ## First set of linear data before first gap
        if igap[0]-0 >= data_length: # Only add data if set is long enough
            isplit = np.arange(0, igap[0]) # begining of data to begining of gap
            xsplit.append(x[isplit])
            ysplit.append(y[isplit])
            isplit_all.append(isplit)
        else: 
            if verbose: print('data_split: First set exluded as too short')

        ## Deal with linear data that isn't bordered by the ends of the set
        for i in np.arange(1,len(igap)): # if start=stop, loop over empty array -> do nothing when len(ifap)=1
            ## Note: arange doesn't include stop, so len 2 just loops over i=1
            if igap[i]-igap[i-1]+1 >= data_length: # Only add data if set is long enough
                isplit = np.arange(igap[i-1]+1, igap[i]) # end of last gap begining of next gap
                xsplit.append(x[isplit])
                ysplit.append(y[isplit])
                isplit_all.append(isplit)
            else: 
                if verbose: print('data_split: Set {} exluded as too short'.format(i))

        ## Last set of linear data after last gap
        if (len(x)-1)-igap[-1]+1 >= data_length: # Only add data if set is long enough
            isplit = np.arange(igap[-1]+1, len(x)-1) # end of last gap to end of data
            xsplit.append(x[isplit])
            ysplit.append(y[isplit])
            isplit_all.append(isplit)
        else: 
            if verbose: print('data_split: Last set exluded as too short')

    return isplit_all, xsplit, ysplit

def smooth(x, window_len=10, window='hanning'):
    """smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal

    example:

    import numpy as np
    t = np.linspace(-2,2,0.1)
    x = np.sin(t)+np.random.randn(len(t))*0.1
    y = smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    """
    # print('\n\nIn tf_data.smooth()\n\n')
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    # s=np.r_[2*x[0]-x[window_len:1:-1], x, 2*x[-1]-x[-1:-window_len:-1]]  # original
    s=np.r_[2*x[0]-x[window_len-1::-1], x, 2*x[-1]-x[-1:-(window_len+1):-1]]
    #print(len(s))
    assert(len(s) == len(x) + 2*window_len)

    if window == 'flat': #moving average
        w = np.ones(window_len,'d')
    else:
        w = getattr(np, window)(window_len)
    y = np.convolve(w/w.sum(), s, mode='same')  # len(y) = len(s)-2 ?
    # return y[window_len-1:-window_len+1]  # original
    y = y[window_len:-window_len]
    assert(len(y) == len(x))
    return y

def smooth2(x, window_len=11, polyorder=2, deriv=0, delta=1.0, axis=-1, mode='interp', cval=0.0):
    y = savgol_filter(x, window_len=window_len, polyorder=polyorder, mode=mode, cval=cval)
    return y

def flinear(x, m, c):
    """ Linear function: m*x + c """
    return m*x + c

def fquadratic(x, a, b, c):
    return a*x**2 + b*x + c

def fsqrt(x, a, b):
    return a*x**0.5 + b

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
    print('*** tf_data.py demo ***')
    x = np.linspace(0,1000,1000)
    y = np.sin(np.deg2rad(x))#+x
    y = y/np.amax(np.absolute(y)) 
    x = x
    print("interp_val(x, y, 2.3649, kind='linear') = ", end=' ')
    print(interp_val(x, y, 2.3649, kind='linear'))

    fig = plt.figure('conv_diff test')
    fig.clear()
    plt.plot( x, y, label = 'sin', c='k', lw=3)
    for n in range(4):
        plt.plot(x, conv_diff(y, order=n), label='n={}'.format(n))
    plt.title('conv_diff test')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

    x = np.arange(30)
    s = smooth(x, window_len=5)
    print('lenx:', len(x), len(s))

    pass

