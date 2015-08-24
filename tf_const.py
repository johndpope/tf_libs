#!/bin/env python

#==============================================================================
# Purpose: Physical constants and conversion factors
#
# Description:
#  
# Notes:
#  
# Reminders:
#
# Author:   Tom Farley
# Created:  20-08-14
# Modified: 00-00-14  
#==============================================================================

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

if __name__ == "__main__":
    print "e = ", e