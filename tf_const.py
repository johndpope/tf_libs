#!/usr/bin/env python

""" tf_const.py: Physical constants and function forms

Detailed description:

Notes:
    @bug:

Todo:
    @todo:

Info:
    @since: 18/09/2015
"""

import tf_libs.tf_debug as tf_debug
import tf_libs.tf_string as tf_string

__author__ = 'Tom Farley'
__copyright__ = "Copyright 2015, TF Library Project"
__credits__ = []
__email__ = "farleytpm@gmail.com"
__status__ = "Development"
__version__ = "1.0.1"

## CAN import:    debug
## CANNOT import:

db = tf_debug.debug(1,0,0)

""" Physical constants: 
## Physical constants
e   = 1.602176565e-19   # Elementary charge [C]
k_B = 1.3806488e-23     # Boltzman constant = R/N_A [J/K]
N_A = 6.02214129e23     # Avagadros constant [None]
amu = 1.66053886e-27    # Atomic mass unit [kg]
eps_0 = 8.8541878e-12   # Vacuum permittivity (epsilon_0) [F/m]
pi  = 3.1415926535898   # pi 

## Conversion factors
K   = 11604.505         # eV to K conversion factor = e/k_B [K/eV]

## Specific constants
M_Ar = 39.948
"""

## Physical constants
e   = 1.602176565e-19   # Elementary charge [C]
m_e = 9.10938291e-31    # Electron mass [kg]
k_B = 1.3806488e-23     # Boltzman constant = R/N_A [J/K]
N_A = 6.02214129e23     # Avagadros constant [None]
amu = 1.66053886e-27    # Atomic mass unit [kg]
eps_0 = 8.8541878e-12   # Vacuum permittivity (epsilon_0) [F/m]
pi  = 3.1415926535898   # pi 

## Conversion factors
eV2K   = 11604.505         # eV to K conversion factor = e/k_B [K/eV]

## Specific constants
M_Ar = 39.948           # Atomic mass of atomic/molecular Argon [amu]


## Functions
def poly(x, *args, str_eqn=False):
    """ Polynomial function of order len(args)-1
    Return: arg1 + arg2 x + arg3 x^2 + arg4 x^3 + ..."""
    if not args:
        raise('poly requires at least one arguement')

    # db(args=args)
    sum = 0
    pow = 0
    eqn = []
    for arg in args:
        sum += arg * x**pow
        if str_eqn: eqn.insert(0,'{}x^{}'.format(arg,pow))

    
    return sum

def exp(*args):
    pass



if __name__ == "__main__":
    print("e = ", e)