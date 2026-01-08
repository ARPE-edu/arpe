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

import os
import skrf as rf
from algorithm.Phase_Unwrap_Correction import PhaseUnwrappingCorrection
from algorithm.PeakValueFunction import PeakValue
from algorithm.WCCFX import ComplexFit
from algorithm.final_betas import BetaFunction
import algorithm.Dict as Dict
import pandas as pd


def Q(filepath):
    """
    Process a single Touchstone file and compute resonance/quality factors.

    filenames, wccfx_results, plot_data, unloaded_quality_factors, export_df, files_corrupted
    """
    _ , filename = os.path.split(filepath)
    filenames = []
    files = []
    resonance_initial = []
    wccfx_results = []
    plot_data = []
    unloaded_quality_factors = []
    resonances = []
    loaded_quality_factors = []
    coupling_factor_s11 = []
    coupling_factor_s22 = []
    percent_removed = []
    files_corrupted = []

    files.append(filepath)
    filenames.append(filename)
    

    for touchstone in files:
        try:
            # Load Touchstone file
            ring_slot = rf.Network(touchstone)

            # Convert to DataFrame
            df = ring_slot.to_dataframe()

            # Initial resonance estimation (scalar)
            resonance_initial = PeakValue(df)
        
            # Phase unwrapping correction
            [S11_corr, S21_corr, _, S22_corr, tau] = PhaseUnwrappingCorrection(ring_slot, df)

            # Weighted complex circle fit extraction
            [resonance_frequency, loaded_qfactor, real_S21_origin, imag_S21_origin, real_S21_wccfx, imag_S21_wccfx, percantage] = ComplexFit(ring_slot,resonance_initial,df,S21_corr[0])

            # Beta function (coupling factors)
            [beta1, beta2, real_S11, imag_S11, S11_circle_real, S11_circle_imag, S11_circ_center_real, S11_circ_center_imag, real_S22, imag_S22, S22_circle_real, S22_circle_imag, S22_circ_center_real, S22_circ_center_imag, freq_band, S11_dB_raw, S22_dB_raw, S21_db_raw] = BetaFunction(ring_slot, df, S11_corr[0], S22_corr[0], S21_corr[0], tau, 1, resonance_frequency, loaded_qfactor)

            # Aggregate data for plotting/return
            plot_data.append((real_S21_origin, imag_S21_origin, real_S21_wccfx, imag_S21_wccfx, real_S11, imag_S11, S11_circle_real, S11_circle_imag, S11_circ_center_real, S11_circ_center_imag, real_S22, imag_S22, S22_circle_real, S22_circle_imag, S22_circ_center_real, S22_circ_center_imag, freq_band, S11_dB_raw, S22_dB_raw, S21_db_raw))
            wccfx_results.append((resonance_frequency, loaded_qfactor))
            resonances.append(resonance_frequency)
            loaded_quality_factors.append(loaded_qfactor)
            coupling_factor_s11.append(beta1)
            coupling_factor_s22.append(beta2)
            unloaded_quality_factors.append(loaded_qfactor * (1 + beta1 + beta2))
            percent_removed.append(percantage)
        
        except:
            print("ERROR!")
            files_corrupted.append(touchstone)
            continue

    # Remove corrupt files from the list of processed files
    for corruptfile in files_corrupted:
        files.remove(corruptfile)

    # Prepare DataFrame for saving
    data = {"Filenames": filenames, "Resonant Frequency": resonances, "Loaded Quality Factor": loaded_quality_factors,
            "Coupling Factor S11": coupling_factor_s11, "Coupling Factor S22": coupling_factor_s22,
            "Unloaded Quality Factor": unloaded_quality_factors,
            "Percentage of Data Removed": percent_removed}
    export_df = pd.DataFrame(data)

    return filenames, wccfx_results, plot_data, unloaded_quality_factors, export_df, files_corrupted

