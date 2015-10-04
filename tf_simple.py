#!/usr/bin/env python

""" tf_array.py: Frequently used array operations and wrappers.

Detailed description:

Notes:
    @bug:

Todo:
    @todo: sub_arr(arr, between=[start, end]) using extract

Info:
    @since: 17-06-14
"""

import numpy as np                  # Maths library

__version__ = "1.0.1"
__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"


def make_iter(obj):
    """ In order to itterate over an object which may be a single item or a tuple of items nest a single item in a
    tuple """

    if hasattr(obj, '__iter__'):
        return obj
    else:
        return (obj,)