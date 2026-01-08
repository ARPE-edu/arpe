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

import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np
from numpy import mean, sqrt

from algorithm.dBCutter import BandWidthCutter


def ComplexFit(ring_slot,resonance_initial,df,S21_corr):
    
    """
    Weighted complex circle fit with iterative outlier removal.

    Args:
        ring_slot: skrf.Network
        resonance_initial: initial resonance estimate (same units as df index)
        df: DataFrame from ring_slot.to_dataframe()
        s21_in: complex ndarray (e.g., corrected S21 trace)

    Returns:
        resonance_iterative, ql_wccfx, np.real(S21_origin), np.imag(S21_origin), S21_wccfx.real, S21_wccfx.imag, Percantage
    """

    #######################################################
    ######## Bandwidth cutter
    #######################################################
    [ _, df_cut_10x3dB, S21_cut_10x3dB] = BandWidthCutter(ring_slot,df,S21_corr)

    # S21 values from the S-Parameter Matrix in .s2p file
    real_S21_cut_10x3dB = S21_cut_10x3dB.real # X = REAL part of S21
    imag_S21_cut_10x3dB = S21_cut_10x3dB.imag # Y = IMAGINARY part of S21

    # move complex circle towards origin
    origin_move_real = abs(0.5*(real_S21_cut_10x3dB[0]+real_S21_cut_10x3dB[-1]))
    origin_move_imag = abs(0.5*(imag_S21_cut_10x3dB[0]+imag_S21_cut_10x3dB[-1]))

    real_S21_origin = np.array([x-origin_move_real for x in real_S21_cut_10x3dB])
    imag_S21_origin = np.array([y-origin_move_imag for y in imag_S21_cut_10x3dB])
    S21_origin = np.array([z-complex(origin_move_real,origin_move_imag) for z in S21_cut_10x3dB])

    frequencies_cut_10x3dB = df_cut_10x3dB['s_db 21'].index
    delta = np.array(0.5*((frequencies_cut_10x3dB/resonance_initial)-(resonance_initial/frequencies_cut_10x3dB)))
    resonance_iterative = resonance_initial

    number_of_iterations = 0
    Anchor = True
    number_points_origin = len(real_S21_origin)


    while Anchor == True:
        number_of_iterations = number_of_iterations + 1
        
        # Matrix formulation
        col1 = np.append(np.ones(len(imag_S21_origin))*real_S21_origin, np.zeros(len(real_S21_origin))*imag_S21_origin)
        col2 = np.append(np.zeros(len(imag_S21_origin))*real_S21_origin, np.ones(len(real_S21_origin))*imag_S21_origin)
        col3 = np.append(-2*delta*real_S21_origin, np.zeros(len(real_S21_origin))*imag_S21_origin)
        col4 = np.append(np.zeros(len(imag_S21_origin))*real_S21_origin, 2*delta*imag_S21_origin)
        col5 = np.append(-2*imag_S21_origin*real_S21_origin, 2*real_S21_origin*imag_S21_origin)
        col6 = np.append(2*imag_S21_origin*delta*real_S21_origin, -2*real_S21_origin*delta*imag_S21_origin)
        
        A_S21_matrix = np.column_stack((col1, col2, col3, col4, col5, col6))
        A_S21_matrix_pseudoinverse = np.linalg.pinv(A_S21_matrix)
        
        b_vector = np.append(real_S21_origin*real_S21_origin, imag_S21_origin*imag_S21_origin)
        x_vector_fitparams = A_S21_matrix_pseudoinverse.dot(b_vector)

        """ Fit parameters extraction """
        """
        x_vector_fitparams[0] → F_re
        x_vector_fitparams[1] → F_im
        x_vector_fitparams[2] → C_im * Q_L
        x_vector_fitparams[3] → C_re * Q_L
        x_vector_fitparams[4] → Q_L * δ_e
        x_vector_fitparams[5] → Q_L
        """

        ql_wccfx = x_vector_fitparams[5]
        delta_e = x_vector_fitparams[4]/ql_wccfx

        delta_f = resonance_iterative * delta_e
        resonance_iterative = resonance_iterative + delta_f

        ## G = K and C = G in the publication
        C_re = x_vector_fitparams[3] / ql_wccfx
        C_im = x_vector_fitparams[2] / ql_wccfx
        C = complex(C_re, C_im)

        F_re = x_vector_fitparams[0]
        F_im = x_vector_fitparams[1]
        F = complex(F_re, F_im)

        G = F - C + complex(0, 2*ql_wccfx*C*delta_e)

        S21_wccfx = (G/(1 + (2j * ql_wccfx * (delta - delta_e))) + C)

        s21new = list(S21_origin)
        frequency = list(frequencies_cut_10x3dB)
        S21_origin = s21new
        frequencies_cut_10x3dB = frequency
        max_s21_magnitude = max(abs(z) for z in S21_origin)

        Prover = []
        for j in range(len(S21_origin)):
            Prover.append(abs(abs(S21_origin[j]-C)**(-1) - abs(S21_wccfx[j] - C)**(-1)))

        Th = 10
        condition =  (Th*max_s21_magnitude)**(-1)
        
        if  max(Prover) < condition :
            Percantage = (100 - ((100 / number_points_origin) * len(real_S21_origin)))
            
            break
        else:
            del S21_origin[Prover.index(max(Prover))]
            real_S21_origin = np.real(S21_origin)
            imag_S21_origin = np.imag(S21_origin)
            del frequencies_cut_10x3dB[Prover.index(max(Prover))]
            delta = np.array(0.5 * ((frequencies_cut_10x3dB / resonance_iterative) - (resonance_iterative / frequencies_cut_10x3dB)))

    ################## ???? 
    # # Circle fitting with scipy.optimize.leastsq
    # x_m = mean(S21_wccfx.real)
    # y_m = mean(S21_wccfx.imag)

    # def calc_R(xc, yc):  # calculate the distance of each 2D points from the center (xc, yc)
    #     return sqrt((S21_wccfx.real - xc) ** 2 + (S21_wccfx.imag - yc) ** 2)

    # def f_2(c):  # calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc)
    #     Ri = calc_R(*c)
    #     return Ri - Ri.mean()

    # center_estimate = x_m, y_m  # Find barycenter
    # center_2, ier = optimize.leastsq(f_2, center_estimate)

    # xc, yc = center_2  # Circle Fit center
    # R_2 = calc_R(*center_2).mean()  # Circle Fit radius
    # t = np.linspace(0, 2 * np.pi, len(df) + 1)
    #x_c = R_2 * np.cos(t) + xc
    #y_c = R_2 * np.sin(t) + yc

    #GMAG = np.sqrt(G.real**2 + G.imag**2)

    return resonance_iterative,ql_wccfx,np.real(S21_origin), np.imag(S21_origin),S21_wccfx.real, S21_wccfx.imag, Percantage