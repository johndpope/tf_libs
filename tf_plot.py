#!/bin/env python

#==============================================================================
# Purpose: 
#
# Description:
#  
# Notes: Make histogram of array elements function
#
# Reminders:
#
# Author:   Tom Farley
# Created:  00-00-14
# Modified: 00-00-14  
#==============================================================================

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib                   # For transforms etc ?
from matplotlib import transforms   # For transforms etc

import tf_numeric as tf_num


def vline_label(x, label, ypos=0.8, xoffset=0.01, color = 'k'):
    """ Plot labeled vline, x in data coordinates, y in axis coordinates """
    fig = plt.gcf()
    ax = plt.gca()
    xlim = plt.xlim() # could use ax.get_xlim()
    xran = xlim[1] - xlim[0]
    # The x coords of this transformation are data, and the y coord are axes
    transy = transforms.blended_transform_factory(
                        ax.transData, ax.transAxes)  
    plt.axvline( x, linestyle='--', color = color)    
    plt.text(x+xoffset*xran, ypos, label, transform=transy, color = color ) 

def new_axis( ):
	"""
	Make new plot and reuturn its axes - used for finding axes ranges etc:

	CODE:
	fig = plt.figure()
	ax = fig.add_subplot(111)
	"""
	fig = plt.figure()
	ax = fig.add_subplot(111)
	return ax

def text_poss( x, y, string, ax, center = False ):
	""" Given a string, an axis, and fractional axis coordinates, plot text 
	at those coordiantes (eg 20% from left, 20% from bottom)  
	ie will plot text string at:
	x_data = x_min + x_range * x_frac
	y_data = y_min + y_range * y_frac

	Inputs:
        string:   	string to add to plot
        ax:			axis of the current plot (in order to get limits)
        x: 			fractional x coordiante at which to plot string
        y: 			fractional y coordiante at which to plot string
    Outputs:
        NONE. (plots text) 
	"""

	if center == True:
		plt.text( x, y, string, 
				horizontalalignment='center', verticalalignment='center',
				transform=ax.transAxes)
	else:
		plt.text( x, y, string, 
				transform=ax.transAxes)
	## Get axis limits
	# ax_limits = ax.axis()
	# x_data = tf_num.frac_range( ax_limits[0:2], x )
	# y_data = tf_num.frac_range( ax_limits[2:4], y )
	# plt.text( string, x_data, y_data )

def axis_range( x, pad1=5, pad2=10 ):
	""" Old function that takes data
	"""
    ## Pad percentage values
	pad1 /= 100.0 # Convert to percentage
	pad2 /= 100.0
	range = tf_num.range_of(x)
	return [ min(x)-pad1*range, max(x)+pad2*range]
	
def arr_hist(arr, nbins=50):

	# the histogram of the data with histtype='step'
	n, bins, patches = plt.hist(arr, nbins, normed=1, histtype='stepfilled')
	plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

	mean = np.mean(arr)
	# mode = sp.stats.mode(arr)
	min = np.min(arr)
	max = np.max(arr)
	range = max-min
	stdev = np.std(arr)
	stats_str = 'Mean: {:0.1f}\nMode: \nMin: {:0.1f}\nMax: {:0.1f}\nRange: {:0.1f}\nStd dev: {:0.1f}'.format(mean, min, max, range, stdev)
	plt.annotate(stats_str, xy=(0.04, 0.75), xycoords='axes fraction')

	plt.show()

	# add a line showing the expected distribution
	# y = sp.stats.normpdf( bins, mu, sigma)
	# l = plt.plot(bins, y, 'k--', linewidth=1.5)
	return


if __name__ == "__main__":
	print("axis_range([0,1,2,3,10])")
	print(axis_range([0,1,2,3,10]))

	mu, sigma = 200, 25
	x = mu + sigma*np.random.randn(10000)
	# x = np.linspace(0,100)
	arr_hist((x, x*0.75))







