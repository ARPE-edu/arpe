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

import numpy as np
import pandas as pd


def PeakValue(df: pd.DataFrame) -> float:
    """
    Return the resonant frequency as the index value at which S21 (in dB)
    reaches its maximum.

    Expects a column named 's_db 21' as produced by skrf.Network.to_dataframe().
    """
    col = 's_db 21'
    if col not in df.columns:
        raise KeyError(f"Required column '{col}' not found in DataFrame.")

    # Index of maximum S21 value → resonant frequency (Hz)
    resonant_freq = df[col].idxmax()
    return float(resonant_freq)






