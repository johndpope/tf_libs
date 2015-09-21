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

import tf_array
import tf_plot as tfp
from tf_debug import debug as tfdebug


__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"

class PhysQuant(object):
    def __init__(self, name, symbol, unit):
        self.name  = name
        self.symbol = symbol
        self.unit  = unit


class ParamFloat():
    """ Experimental parameter of float type """

    def __init__(self, value, phys_quant, error=None, fn=None):
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

class Plot(object):
    def __init__(self, x=None, y=None, title = None, subplot=111):
        self.ax, self.fig = tfp.new_axis(subplot)
        self.title = title
        
        if x:
            assert type(x) == ParamFloat, 'Plotted variables must be of type ParamFloat'
        
        if self.title:
            self.set_title(title)

        # self.fig.show()
        plt.draw()

    def set_title(self,title):
        assert type(title) == str, 'title must be a string'
        # self.fig.title = title
        plt.title = title

class PlotLines(Plot):
    def __init__(self):
        pass


class Plot3D(Plot):
    def __init__(self, z=None):
        pass

if __name__ == "__main__":
    pass