"""
Algorithm for Resonator Parameter Extraction from Symmetrical and Asymmetrical Transmission Responses
by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan, 2021

Code written by Patrick Krkotic and Queralt Gallardo
arpe-edu@outlook.de

Version 1.0.0
Contributors:

Developed on Python 3.7.7
"""

import control
import numpy as np


def PeakValue(df):

###############################################################
#### Frequency Determination over maximum of S21
###############################################################

    #max = df['s_db 21'].max()  # Maxim value of S21
    fo = df['s_db 21'].idxmax()  # Frequency at the maximum = resonant frequency


    return fo





