"""
Algorithm for Resonator Parameter Extraction from Symmetrical and Asymmetrical Transmission Responses
by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan, 2021

Code written by Patrick Krkotic and Queralt Gallardo
arpe-edu@outlook.de

Version 1.0.0

Contributors:

Developed on Python 3.7.7
"""


import skrf as rf
from pandas import *
import pandas as pd
from scipy.interpolate import *
import control
import matplotlib.pyplot as plt
import pylab
from colorama import Fore, Back, Style
import numpy as np



def BandWidthCutter(ring_slot,df,S21):
    ############################################## MAX - F0 ##########################################################
    try:
        max = df['s_db 21'].max() # Maxim value of S21
        fo = df['s_db 21'].idxmax() # Frequency at the maximum = resonant frequency

        # Values to interpolate
        x = df['s_db 21'].index # x = frequencies
        xx = x.to_numpy()
        y = df['s_db 21'].values # y = values

        # Find the points at -3dB
        value_3db = max - 3.0

        t = np.where(y == max)
        xleft = x[0:t[0][0]]
        yleft = y[0:t[0][0]]
        xright = x[t[0][0]:]
        yright = y[t[0][0]:]


        ff1 = np.interp(value_3db,yleft,xleft)
        ff2 = np.interp(value_3db, np.flip(yright), np.flip(xright))
        bw3db = ff2 - ff1

        TotalWidth = abs(x[0] - x[-1])

        if TotalWidth > 10 * bw3db:
            # print(" Bandwidth Cut Activated ")
            Left = fo - 5 * bw3db
            Right = fo + 5 * bw3db
            x = x[(x >= Left) & (x <= Right)]
            df = df[df.index.isin(x)]

            ringleft = np.where(xx == x[0])
            ringright = np.where(xx == x[-1])
            ring_slotcut = ring_slot.s[ringleft[0][0]:ringright[0][0] + 1, 1, 0]
            S21cut = S21[ringleft[0][0]:ringright[0][0] + 1]

        else:
            df = df
            ring_slotcut = ring_slot.s[:, 1, 0]
            S21cut = S21

        return ring_slotcut, df, S21cut

    except:
        print('Data Cut has failed!')
        return ring_slot, df, S21
        



def BandWidthCutterTwo(ring_slot, df):
    ############################################## MAX - F0 ##########################################################
    max = df['s_db 21'].max() # Maxim value of S21
    fo = df['s_db 21'].idxmax() # Frequency at the maximum = resonant frequency

    # Values to interpolate
    x = df['s_db 21'].index # x = frequencies
    xx = x.to_numpy()
    y = df['s_db 21'].values # y = values

    value_10db = max - 3

    t = np.where(y == max)
    xleft = x[0:t[0][0]]
    yleft = y[0:t[0][0]]
    xright = x[t[0][0]:]
    yright = y[t[0][0]:]

    TotalWidth = abs(x[0] - x[-1])

    ff1 = np.interp(value_10db,yleft,xleft)
    ff2 = np.interp(value_10db, np.flip(yright), np.flip(xright))
    bw10db = ff2 - ff1
    if TotalWidth > bw10db:
        Left = fo - 0.5 * bw10db
        Right = fo + 0.5 * bw10db
        x = x[(x >= Left) & (x <= Right)]
        df = df[df.index.isin(x)]

        ringleft = np.where(xx == x[0])
        ringright = np.where(xx == x[-1])
        ring_slotcut11 = ring_slot.s[ringleft[0][0]:ringright[0][0]+1, 0, 0]
        ring_slotcut22 = ring_slot.s[ringleft[0][0]:ringright[0][0]+1, 1, 1]

    else:
        df = df
        ring_slotcut11 = ring_slot.s[:, 0, 0]
        ring_slotcut22 = ring_slot.s[:, 1, 1]

    return ring_slotcut11,ring_slotcut22,df