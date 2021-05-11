"""
Novel Algorithm for Resonator Parameter Extraction with Outlier Removal
by Patrick Krkotić, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O’Callaghan, 2020

Code written by Patrick Krkotić and Queralt Gallardo
patrickkrkotic@outlook.de

Developed on Python 3.7.7
"""

import control
import numpy as np




def Lorentz(df):
###############################################################
#### Frequency Determination over maximum of S21
###############################################################

    max = df['s_db 21'].max()  # Maxim value of S21
    fo = df['s_db 21'].idxmax()  # Frequency at the maximum = resonant frequency
    print('this is the max freqpoint' + str(fo))


    return fo





