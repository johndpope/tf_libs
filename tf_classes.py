#!/usr/bin/env python

""" tf_classes.py:

Detailed description: Data manipulation classes

Notes:
    @bug:

Todo:
    @todo: Use param module
    @todo: Use scipy units


Info:
    @since: 20/09/2015
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
import copy

from pprint import pprint  # Pretty printing

## CAN import:    all tf_* files
## CANNOT import: None
import tf_array
import tf_plot as tfp
import tf_debug

__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"

db = tf_debug.debug(1,0,0)

class PhysQuant(object):
    def __init__(self, name, symbol, unit):
        self.name  = name
        self.symbol = symbol
        self.unit  = unit


class ParamFloat():
    """ Experimental parameter of float type """

    def __init__(self, value, phys_quant, error=None, fn=None, description=None):
        self.value = value

        if type(phys_quant) == str:
            self.phys_quant = self.get_dflt_phys_quant(phys_quant)
            self.name = self.phys_quant.name
            self.symbol = self.phys_quant.symbol
            self.unit = self.phys_quant.unit
        elif len(phys_quant) == 3:
            self.phys_quant = PhysQuant(phys_quant[0],phys_quant[1],phys_quant[2])
            self.name = phys_quant[0]
            self.symbol = phys_quant[1]
            self.unit = phys_quant[2]
        else:
            assert (type(phys_quant) == str) or (len(phys_quant) == 3), 'Incorrect type/format for phys_quant'

        self.error = error
        self.fn    = fn
        self.description = description

        # self.lname = name.lower()
        # self.uname = name.capitalize()
        # self.label = (name+' ['+unit+']').encode('string-escape') if (not unit == '') else name
        # self.equals = (name+' = '+repr(value)+' '+unit).encode('string-escape')
        # self.fn    = params

    def __repr__(self):
        return 'ParamFloat<'+self.name+'> object'

    def __str__(self):
        #print help(self.value)
        return self.name+' = '+repr(self.value)+' '+self.unit

    def __call__(self):
        " Value of float parameter "
        return self.value

    def __getitem__(self,index):
        if tf_array.is_scalar(self.value):
            raise IndexError('This <float parameter> is scalar and cannot be indexed')
        return self.value[index]

    def __len__(self):
        """ Length of parameter value array """
        return tf_array.safe_len(self.value)

    def __copy__(self):
        ## Shallow copy
        return type(self)(self.name, self.unit, self.value, fn=self.fn)

    def __deepcopy__(self):
        ## Broken?
        return copy.deepcopy(type(self)(self.name, self.unit, self.value, fn=self.fn))

    def __del__(self):
        """ Unfinished """
        class_name = self.__class__.__name__

    def valueSI(self):
        if self.unit == 'mTorr':
            return self.value * 133.3224e-3
        elif self.unit == 'eV':
            return self.value * 1.60217657e-19 / 1.3806488e-23

    def label(self):
        return self.name+' ['+self.unit+']'

    def legend(self):
        """ Return description of parameter appropriate for a plot legend """
        if self.description:
            return self.description
        else:
            return self.name

    def val_unit(self):
        return repr(self.value)+' '+self.unit

    def update(self, value):
        self.value = value

    def info(self):
        pprint (vars(self))

    def get_dflt_phys_quant(self, symbol):
        dflts = {
            'arb':('Arbitrary quantity', 'No units'),
            'I':('Current','A'),
            't':('Time', 's'),
            'P':('Probability', None),
            'x':('X coordinate', 'm'),
            'y':('Y coordinate', 'm'),
            'z':('Z coordinate', 'm')
                 }
        assert symbol in dflts.keys(), 'Symbol for physical quantity not recognised'

        return PhysQuant(dflts[symbol][0],symbol,dflts[symbol][1])




class Param_string:
    """ Experimental parameter of string type """

    def __init__(self, name, value, fn=None):
        self.name  = name
        self.value = value
        self.fn    = fn

        self.lname = name.lower()
        self.uname = name.capitalize()
        self.label = name
        self.equals = name+' = '+repr(value)
        # self.fn    = params

    def __repr__(self):
        return 'ParamFloat<'+self.name+'> object'

    def __str__(self):
        return 'ParamFloat<'+self.Name+'>'

    def __del__(self):
        class_name = self.__class__.__name__

    def info(self):
        pprint (vars(self))


class Data(object):
    """ Ideas to include:
    - Key atributes: x, y, z, x_err, y_err, z_err, y_fit, z_fit
    - Auto data fit atribute
    - methods: average, differentiate, subtract given columns etc
    """

class Plot(object): # Inherit plt.figure ?
    def __init__(self, x=None, y=None, title = None, subplot=111, defaults=1):
        ## Check arguments are as expected
        if x: assert type(y) == ParamFloat or (type(y) == tuple and type(y[0])==ParamFloat), 'y plotting variable must be a <ParamFloat> or tuple of <ParamFloat>s'
        if y: assert type(y) == ParamFloat or (type(y) == tuple and type(y[0])==ParamFloat), 'y plotting variable must be a <ParamFloat> or tuple of <ParamFloat>s'

        ## Store arguments in self
        self.title = title
        self.x = x
        self.y = tf_array.make_tuple(y) # Always make y a tuple even if it only contains one set of data

        ## Set default mpl properties (font sizes etc)
        tfp.set_mpl_defaults(defaults=defaults)
        plt.ion() # Interactive plotting (draw implicit)

        ## Create the figure and axes
        self.ax, self.fig = tfp.new_axis(subplot)

        ## Set axis title and labels
        if self.title:
            self.set_title(title)
        if self.x:
            self.set_xlabel(self.x.label())
        if self.y:
            self.set_ylabel(self.y[0].label()) # set y axis using first y parameter in tuple

            # self.fig.show()
            # plt.draw()
            # plt.show()

    def set_title(self,title):
        assert type(title) == str, 'title must be a string'
        self.ax.set_title(title)

    def set_xlabel(self,xlabel):
        assert type(xlabel) == str, 'xlabel must be a string'
        self.ax.set_xlabel(xlabel)

    def set_ylabel(self,ylabel):
        assert type(ylabel) == str, 'ylabel must be a string'
        self.ax.set_ylabel(ylabel)

    def text(self, x, y, string, center = False):
        """ Add text to plot at given plot coordinates """
        tfp.text_poss(x, y, string, self.ax, center = False)

    def save_fig(self, dir_fig='./Figures/', fn='Figure_tmp', ext='.png', dpi=300, silent=False, create_dir=False):
        """ Save figure as an image """
        tfp.save_fig(self.fig, dir_fig=dir_fig, fn=fn, ext=ext, dpi=dpi, silent=silent, create_dir=create_dir)


class PlotLines(Plot):
    def __init__(self, cm = 'jet', padx = [5, 5], pady = [5, 5], pass_zero=0, force_legend=False, **kwargs):

        self.lines = []

        super().__init__(**kwargs) # Run __init__ for Plot base class

        self.plot2D() # Plot the data
        self.update_colours(cm=cm) #
        self.update_ranges(padx = padx, pady = pady, pass_zero=pass_zero) # Extend the axes ranges
        self.add_legend(force_legend=force_legend)
        self.text(0.1, 0.9, 'Here is some text')
        self.save_fig(create_dir=True, dpi=300)
        plt.show()

    def plot2D(self):
        """ Plot the y parameters (stored in a tuple) vs the x parameter """

        for y in self.y: # Loop over y parameters and plot a line for each (a single y param is nested in a tuple)
            line = self.ax.plot(self.x.value, y.value, label=y.legend())
            self.lines.append(line)

    def update_colours(self, cm='jet'):
        tfp.update_colors(self.ax, cm=cm)

    def update_ranges(self, padx = [5, 5], pady = [5, 5], pass_zero=0):
        """ Update axis ranges """
        tfp.axis_range(self.ax, padx = padx, pady = pady, pass_zero=pass_zero)

    def add_legend(self, force_legend = False):
        """ Add legend to plot with default setting (best position, dragable, transparrent etc)
        """
        if len(self.lines) > 1 or force_legend: # Only show the legend if there is more than one plot
            tfp.legend_dflt(self.ax)


class Plot3D(Plot):
    def __init__(self, z=None):
        pass

if __name__ == "__main__":
    pass