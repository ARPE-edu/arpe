"""
Algorithm for Resonator Parameter Extraction from
Symmetrical and Asymmetrical Transmission Responses

Authors:
    Patrick Krkotic
    Queralt Gallardo
    Nikki Tagdulang
    Montse Pont
    Joan M. O'Callaghan

Contributors:
    Agustin Gomez Mansilla
    Martin Herold
    Tamas Madarasz

Contact:
    arpe-edu@outlook.de

Original Publication:
    2021

Version History:
    v1.0.0  – Initial release (Python 3.7.7) - 2021
    v2.0.0  – New interface and updated to Python 3.11.9 - 2023
    v2.1.0  – Novel routine for over and undercoupling, refactoring and clean-up, and update to Python 3.12.10 - 2026

Citation:
    Please cite the original 2021 publication when using this code.
"""


from pandas import *
from scipy.interpolate import *
import numpy as np



def BandWidthCutter(ring_slot,df,S21):

    """
    Cut data to a window around the -3 dB bandwidth (±5 * BW) if the total
    span is much larger than the bandwidth.

    Returns:
        ring_slotcut (complex ndarray): ring_slot.s cut to the selected band (S21)
        df_cut (DataFrame): df cut to the same band
        s21_cut (complex array/list): provided s21 cut to the same band
    """
        
    try:
        peak_dB = df['s_db 21'].max() # Maxim value of S21
        resonance_at_peak = df['s_db 21'].idxmax() # Frequency at the maximum = resonant frequency

        # Values to interpolate
        frequencies = df['s_db 21'].index
        frequencies_np = frequencies.to_numpy()
        S21_dB = df['s_db 21'].values # y = values

        # Find the points at -3dB
        target_3dB = peak_dB - 3.0

        t = np.where(S21_dB == peak_dB)
        frequencies_left = frequencies[0:t[0][0]]
        S21_left = S21_dB[0:t[0][0]]
        frequencies_right = frequencies[t[0][0]:]
        S21_right = S21_dB[t[0][0]:]


        freq_3dB_left = np.interp(target_3dB,S21_left,frequencies_left)
        freq_3dB_right = np.interp(target_3dB, np.flip(S21_right), np.flip(frequencies_right))
        bw_3dB = freq_3dB_right - freq_3dB_left

        freq_span = abs(frequencies[0] - frequencies[-1])
        
        # Cut the data to 10 x the 3dB bandwidth around the peak resonance value
        if freq_span > 10 * bw_3dB:
            Left = resonance_at_peak - 5 * bw_3dB
            Right = resonance_at_peak + 5 * bw_3dB
            frequencies = frequencies[(frequencies >= Left) & (frequencies <= Right)]
            df_cut_10x3dB = df[df.index.isin(frequencies)]

            ringleft = np.where(frequencies_np == frequencies[0])
            ringright = np.where(frequencies_np == frequencies[-1])
            ring_slotcut = ring_slot.s[ringleft[0][0]:ringright[0][0] + 1, 1, 0]
            S21_cut_10x3dB = S21[ringleft[0][0]:ringright[0][0] + 1]

        else:
            df_cut_10x3dB = df
            ring_slotcut = ring_slot.s[:, 1, 0]
            S21_cut_10x3dB = S21

        return ring_slotcut, df_cut_10x3dB, S21_cut_10x3dB

    except:
        print('Data Cut has failed!')
        return ring_slot, df, S21
        



def BandWidthCutterTwo(ring_slot, df):
    """
    Cut reflection data (S11/S22) to a ±0.5 * BW window around the peak,
    where BW is computed at -3 dB from S21.
    """
    peak_dB = df['s_db 21'].max() # Maxim value of S21
    resonance_at_peak = df['s_db 21'].idxmax() # Frequency at the maximum = resonant frequency

    # Values to interpolate
    frequencies = df['s_db 21'].index # x = frequencies
    frequencies_np = frequencies.to_numpy()
    S21_dB = df['s_db 21'].values # y = values

    value_3dB = peak_dB - 3

    t = np.where(S21_dB == peak_dB)
    frequencies_left = frequencies[0:t[0][0]]
    S21_left = S21_dB[0:t[0][0]]
    frequencies_right = frequencies[t[0][0]:]
    S21_right = S21_dB[t[0][0]:]

    freq_span = abs(frequencies[0] - frequencies[-1])

    freq_3dB_left = np.interp(value_3dB,S21_left,frequencies_left)
    freq_3dB_right = np.interp(value_3dB, np.flip(S21_right), np.flip(frequencies_right))

    bw_3dB = freq_3dB_right - freq_3dB_left

    if freq_span > bw_3dB:
        Left = resonance_at_peak - 0.5 * bw_3dB
        Right = resonance_at_peak + 0.5 * bw_3dB
        frequencies = frequencies[(frequencies >= Left) & (frequencies <= Right)]
        df_cut_3dB = df[df.index.isin(frequencies)]

        ringleft = np.where(frequencies_np == frequencies[0])
        ringright = np.where(frequencies_np == frequencies[-1])
        S11_cut_3dB = ring_slot.s[ringleft[0][0]:ringright[0][0]+1, 0, 0]
        S22_cut_3dB = ring_slot.s[ringleft[0][0]:ringright[0][0]+1, 1, 1]

    else:
        df_cut_3dB = df
        S11_cut_3dB = ring_slot.s[:, 0, 0]
        S22_cut_3dB = ring_slot.s[:, 1, 1]

    return S11_cut_3dB,S22_cut_3dB,df_cut_3dB