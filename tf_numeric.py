#!/usr/bin/env python
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

""" tf_numeric.py: Frequently used numeric functions.

Detailed description:

Notes:
    @bug:

Todo:
    @todo:

Info:
    @since: 18/09/2015
"""

import numpy as np
import matplotlib.pyplot as plt


## CAN import: tf_debug
## CANNOT import: tf_array, tf_string

__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"



def range_of(list):
    """ Return the numerical range of a numeric list
    Inputs:
        list:   numeric (python) list or numpy array
    Outputs:
        float:  numeric range of input list 
    """
    return np.abs(max(list) - min(list))

def frac_range(list, frac):
    """ Return the numerical value at a given fraction of the way 
    through the range of a numeric list ie:
    min + (max - min) * frac 

    Inputs:
        list:   numeric (python) list or numpy array
        frac:   float specifying where in range to return value
    Outputs:
        float:  numeric range of input list 
    """
    return min(list) + (max(list) - min(list)) * frac 


def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    From: http://wiki.scipy.org/Cookbook/SignalSmooth

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y



def smooth_demo():

    t=np.linspace(-4,4,100)
    x=np.sin(t)
    xn=x+np.randn(len(t))*0.1
    y=smooth(x)

    ws=31

    plt.subplot(211)
    plt.plot(np.ones(ws))

    windows=['flat', 'hanning', 'hamming', 'bartlett', 'blackman']

    plt.hold(True)
    for w in windows[1:]:
        eval('plot('+w+'(ws) )')

    plt.axis([0,30,0,1.1])

    plt.legend(windows)
    plt.title("The smoothing windows")
    plt.subplot(212)
    plt.plot(x)
    plt.plot(xn)
    for w in windows:
        plt.plot(smooth(xn,10,w))
    l=['original signal', 'signal with noise']
    l.extend(windows)

    plt.legend(l)
    plt.title("Smoothing a noisy signal")
    plt.show()


if __name__=='__main__':
    smooth_demo()

