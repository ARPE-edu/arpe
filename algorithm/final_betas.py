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



################################### BETAS - REFLECTION CIRCLE FIT ############################################

def BetaFunction(ring_slot,df,S11_corr,S22_corr,S21_corr,tau, MagS21,resonance_frequency, loaded_qfactor):
    
    # keep compatibility for currently-unused inputs but maybe required at later stage
    _ = (tau, MagS21)

    # raw dB traces from network (returned at end)
    S11_dB_raw = ring_slot.s_db[:, 0, 0]
    S22_dB_raw = ring_slot.s_db[:, 1, 1]
    S21_db_raw = ring_slot.s_db[:, 1, 0]

    # magnitudes (dB) from corrected complex traces
    S11_dB = 20*np.log10(np.sqrt(S11_corr.real ** 2 + S11_corr.imag**2))
    S22_dB = 20*np.log10(np.sqrt(S22_corr.real ** 2 + S22_corr.imag**2))
    S21_dB = 20*np.log10(np.sqrt(S21_corr.real ** 2 + S21_corr.imag**2))

    
    # 1) Average S11/S22 in the outer 10% bands, i.e. # 10% lower frequencies + # 10% upper frequencies
    edge_count = int(round(0.1 * len(df)))

    S11_edges = np.concatenate((S11_dB[:edge_count], S11_dB[-edge_count:]), axis=0)
    S22_edges = np.concatenate((S22_dB[:edge_count], S22_dB[-edge_count:]), axis=0)
  
    S11_avg_db = np.mean(S11_edges)
    S22_avg_db = np.mean(S22_edges)
    
    S11_avg_mag = 10 ** (S11_avg_db / 20)
    S22_avg_mag = 10 ** (S22_avg_db / 20)
    
    L_in_avSC = 1 / S11_avg_mag
    L_out_avSC = 1 / S22_avg_mag

    # peak index from S21 trace
    peak_idx = int(np.argmax(S21_dB))

    # minimum S11 and S22 at peak S21
    S11_minimum_dB = S11_dB[peak_idx]
    S22_minimum_dB = S22_dB[peak_idx]

    S11_minimum_mag = 10 ** (S11_minimum_dB / 20)
    S22_minimum_mag = 10 ** (S22_minimum_dB / 20)

    beta1_scalar = (1 - L_in_avSC * S11_minimum_mag) / (L_in_avSC * S11_minimum_mag + L_out_avSC * S22_minimum_mag)
    beta2_scalar = (1 - L_out_avSC * S22_minimum_mag) / (L_in_avSC * S11_minimum_mag + L_out_avSC * S22_minimum_mag)

   
    ############### circle fit S11 and S22 with outlier removal #######################

    frequencies = df['s_db 21'].index
    delta = np.array(0.5 * ((frequencies / resonance_frequency) - (resonance_frequency / frequencies)))

    ringcut = np.where(loaded_qfactor*abs(delta) < 1/2)

    S11_band = ring_slot.s[ringcut[0] , 0, 0]
    S22_band = ring_slot.s[ringcut[0] , 1, 1]
    freq_band = frequencies[ringcut[0]]

    real_S11= S11_band.real
    imag_S11= S11_band.imag
    real_S22= S22_band.real
    imag_S22= S22_band.imag

    # s21 magnitude used for low-signal fallback
    S21_corr_db = 20 * np.log10(np.sqrt(S21_corr.real**2 + S21_corr.imag**2))
    s21_peak_mag = 10 ** (np.max(S21_corr_db) / 20)


    anchor = True    
    while anchor == True:
        A_S11_matrix = np.column_stack((real_S11, imag_S11, np.ones(len(real_S11))))
        b_S11_vector = - (np.sqrt(real_S11 ** 2 + imag_S11 ** 2)) ** 2
        A_S11_matrix_pseudoinverse = np.linalg.pinv(A_S11_matrix)
        x_vector_S11_fitparams = A_S11_matrix_pseudoinverse.dot(b_S11_vector)

        S11_circ_center_real = -x_vector_S11_fitparams[0] / 2
        S11_circ_center_imag = -x_vector_S11_fitparams[1] / 2

        if ((1 / 4) * (x_vector_S11_fitparams[0] ** 2 + x_vector_S11_fitparams[1] ** 2)) - x_vector_S11_fitparams[2] <= 0:
            R11 = 0
        else:
            R11 = np.sqrt(((1 / 4) * (x_vector_S11_fitparams[0] ** 2 + x_vector_S11_fitparams[1] ** 2)) - x_vector_S11_fitparams[2])

        t = np.linspace(0, 2 * np.pi, 2 * len(freq_band) + 1)
        S11_circle_real = R11 * np.cos(t) + S11_circ_center_real
        S11_circle_imag = R11 * np.sin(t) + S11_circ_center_imag

        A_S22_matrix = np.column_stack((real_S22, imag_S22, np.ones(len(real_S22))))
        b_S22_vector = - (np.sqrt(real_S22 ** 2 + imag_S22 ** 2)) ** 2
        A_S22_matrix_pseudoinverse = np.linalg.pinv(A_S22_matrix)
        x_vector_S22_fitparams = A_S22_matrix_pseudoinverse.dot(b_S22_vector)

        S22_circ_center_real = -x_vector_S22_fitparams[0] / 2
        S22_circ_center_imag = -x_vector_S22_fitparams[1] / 2

        if ((1 / 4) * (x_vector_S22_fitparams[0] ** 2 + x_vector_S22_fitparams[1] ** 2)) - x_vector_S22_fitparams[2] <= 0:
            R22 = 0
        else:
            R22 = np.sqrt(((1 / 4) * (x_vector_S22_fitparams[0] ** 2 + x_vector_S22_fitparams[1] ** 2)) - x_vector_S22_fitparams[2])

        S22_circle_real = R22 * np.cos(t) + S22_circ_center_real
        S22_circle_imag = R22 * np.sin(t) + S22_circ_center_imag

        # coef11 = S11_circ_center_real + 1j * S11_circ_center_imag - (R11 * ((S11_circ_center_real + 1j * S11_circ_center_imag) / np.sqrt(S11_circ_center_real ** 2 + S11_circ_center_imag ** 2)))
        #gamma_r_in = np.sqrt(coef11.real ** 2 + coef11.imag ** 2)

        # coef22 = S22_circ_center_real + 1j * S22_circ_center_imag - (R22 * ((S22_circ_center_real + 1j * S22_circ_center_imag) / np.sqrt(S22_circ_center_real ** 2 + S22_circ_center_imag ** 2)))
        #gamma_r_out = np.sqrt(coef22.real ** 2 + coef22.imag ** 2)

        S11_circle_centre = S11_circ_center_real + S11_circ_center_imag*1j
        S22_circle_centre = S22_circ_center_real + S22_circ_center_imag*1j

        Prover_S11 = []
        Prover_S22 = []
        S11_iterative = []
        S22_iterative = []
        new_index_S11 = []
        new_index_S22 = []

        for l in range(len(S11_band)):
            new_index_S11.append(l)

        for index in new_index_S11:
            S11_iterative.append(S11_band[index])

        S11_band = S11_iterative

        for l in range(len(S22_band)):
            new_index_S22.append(l)

        for index in new_index_S22:
            S22_iterative.append(S22_band[index])

        S22_band = S22_iterative

        for k in range(len(S11_band)):
            Prover_S11.append(abs(R11 - abs(S11_band[k] - S11_circle_centre)))

        for k in range(len(S22_band)):
            Prover_S22.append(abs(R22 - abs(S22_band[k] - S22_circle_centre)))

        condition_S11 = 0.1*abs(R11)
        condition_S22 = 0.1*abs(R22)


        if max(Prover_S11) > condition_S11:

            del S11_band[Prover_S11.index(max(Prover_S11))]
            real_S11 = np.real(S11_band)
            imag_S11 = np.imag(S11_band)
        else:
            pass

        if max(Prover_S22) > condition_S22:
            del S22_band[Prover_S22.index(max(Prover_S22))]
            real_S22 = np.real(S22_band)
            imag_S22 = np.imag(S22_band)
        else:
            pass

        if max(Prover_S11) < condition_S11 and max(Prover_S22) < condition_S22:
            break


    # 5. Calculate the coupling factors
    # coef111 = S11_circ_center_real + 1j * S11_circ_center_imag + (R11 * ((S11_circ_center_real + 1j * S11_circ_center_imag) / np.sqrt(S11_circ_center_real ** 2 + S11_circ_center_imag ** 2)))
    # coef222 = S22_circ_center_real + 1j * S22_circ_center_imag + (R22 * ((S22_circ_center_real + 1j * S22_circ_center_imag) / np.sqrt(S22_circ_center_real ** 2 + S22_circ_center_imag ** 2)))

    # print('Losses Circle')
    # L_in_av = 1/np.abs(np.sqrt(coef111.real**2 + coef111.imag**2))
    # L_out_av = 1/np.abs(np.sqrt(coef222.real**2 + coef222.imag**2))

    #SC11 = np.abs((np.abs(co_11) - R11) / (np.abs(co_11) + R11))
    #SC22 = np.abs((np.abs(co_22) - R22) / (np.abs(co_22) + R22))

    # transform circels tangent ot unit circle
    S11_unitcircle_centre = (S11_circle_centre)/(np.abs(S11_circle_centre + R11*(S11_circle_centre/np.abs(S11_circle_centre))))
    R11_unitcircle = (R11)/(np.abs(S11_circle_centre + R11*(S11_circle_centre/np.abs(S11_circle_centre))))

    S22_unitcircle_centre = (S22_circle_centre)/(np.abs(S22_circle_centre + R22*(S22_circle_centre/np.abs(S22_circle_centre))))
    R22_unitcircle = (R22)/(np.abs(S22_circle_centre + R22*(S22_circle_centre/np.abs(S22_circle_centre))))
    
    SC11 = (np.abs(S11_unitcircle_centre) - R11_unitcircle)
    SC22 = (np.abs(S22_unitcircle_centre) - R22_unitcircle) 
     
    beta1_circle = (1 - SC11) / (SC11 + SC22)
    beta2_circle = (1 - SC22) / (SC11 + SC22)

    print(beta1_circle)
    print(beta2_circle)

    beta1 = beta1_circle
    beta2 = beta2_circle

    # If in some rare cases, it appears a negative beta -> beta = 0.0
#################################################################
#     if 0.9 * abs(s11_av) > abs(co_11) :
#    # if Lbeta1SC > 0.01:
#         beta1 = Cbeta1
#     else:
#         beta1 = Wbeta1SC
###### what is this again?
#     #if s22pabs < abs(co_22):
#     if 0.9 * abs(s22_av) > abs(co_22):
#    # if Lbeta2SC > 0.01:
#         beta2 = Cbeta2
#     else:
#         beta2 = Wbeta2SC
#################################################################

    if 20*np.log10(s21_peak_mag) < -50:
        beta1 = beta1_scalar
        beta2 = beta2_scalar

    if beta1_scalar < 0.0 :
        beta1 = 0.0

    if beta2_scalar < 0.0 :
        beta2 = 0.0

    freq_band = df['s_db 21'].index
    return beta1, beta2, real_S11, imag_S11, S11_circle_real, S11_circle_imag, S11_circ_center_real, S11_circ_center_imag, real_S22, imag_S22, S22_circle_real, S22_circle_imag, S22_circ_center_real, S22_circ_center_imag, freq_band, S11_dB_raw, S22_dB_raw, S21_db_raw

