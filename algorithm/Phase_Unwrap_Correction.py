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
import math

def PhaseUnwrappingCorrection(ring_slot,df):
    """
    Phase unwrapping and delay de-embedding for S-parameters.

    Returns:
        s11_corr, s21_corr, s12_corr, s22_corr, tau
        where each sXY_corr is a complex ndarray with delay removed,
        and tau is the estimated average delay (seconds).
    """
        
    s11_phase = []
    s21_phase = []
    s12_phase = []
    s22_phase = []

    #################################################
    #### Touchstone Columns Reminder
    ##################################################

    """
    s11 = ring_slot.s[:,0,0] # S11 values from the S-Parameter Matrix in .s2p file
    s21 = ring_slot.s[:,1,0] # S21 values from the S-Parameter Matrix in .s2p file
    s12 = ring_slot.s[:,0,1] # S12 values from the S-Parameter Matrix in .s2p file
    s22 = ring_slot.s[:,1,1] # S22 values from the S-Parameter Matrix in .s2p file
    """

    #################################################
    #### Phase Unwrapping
    ##################################################

    frequencies = df['s_db 21'].index

    # Permutations 0 0, 0 1, 1 0 , 1 1 --> S11, S12, S21, S22
    for p in range(2):
        for k in range(2):            
            s_parameter = ring_slot.s[:,p,k] 
            phase = ring_slot.s_deg[:,p,k] 
            phase_unwrapped = np.zeros(len(phase))
            j = 0

            # Unwrap routine
            for i in range(len(phase_unwrapped)):
                # Degree to radians
                phase_unwrapped[i] = math.radians(phase_unwrapped[i]) 
            for i in range(len(phase)):
                # Degrees to radians
                phase[i] = math.radians(phase[i]) 

            disc = False
            for i in range(len(phase)-1):
                if phase[i+1] - phase[i] >= ((3*np.pi)/2) or phase[i+1] - phase[i] <= -((3*np.pi)/2): # search for phase discontinuity
                    disc= True
                    if phase[i] < phase[i+1]: # if it is a positive discontinuity
                        j = i
                        for j in range(i, len(phase)-1):
                            phase_unwrapped[j+1] = phase[j+1] - (2*np.pi)
                    else:
                        for j in range(i, len(phase)-1):
                            phase_unwrapped[j+1] = phase[j+1]
                elif disc==False:
                    if i ==0:
                        phase_unwrapped[i] = phase[i]
                        phase_unwrapped[i + 1] = phase[i + 1]
                    else:
                        phase_unwrapped[i+1] = phase[i+1]

            n = round(0.1 * len(df))

            #################################################
            #### Phase Correction
            ##################################################

            ph_ini = phase_unwrapped[:n] # initial 10%
            ph_fin = phase_unwrapped[-n:] # final 10%
            for i in range(len(ph_ini)): # Degrees to radians
                ph_ini[i] = math.radians(ph_ini[i])
                ph_fin[i] = math.radians(ph_fin[i])

            # Linear regression initial part
            coef_lin_ini = np.polyfit(frequencies[:n], ph_ini[:n], 1)
            # Linear regression final part
            coef_lin_fin = np.polyfit(frequencies[-n:], ph_ini[-n:], 1)


            # Plot the phase and its linear fitting INITIAL PART
            """
            plt.figure()
            plt.plot(f[:n], ph_ini, 'ro', label = "S21 phase")
            plt.plot(f[:n], pol_lin_ini(f[:n]), 'b--', label= "S21 phase linear fitting")
            #plt.plot(f[:n], phase, 'm-', label= 'total S21 phase')
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Phase (radians)")
            plt.legend()
            plt.show()
            """

            # Plot the phase and its linear fitting FINAL PART
            """
            plt.figure()
            plt.plot(f[-n:], ph_ini, 'ro', label = "S21 phase")
            plt.plot(f[-n:], pol_lin_fin(f[-n:]), 'b--', label= "S21 phase linear fitting")
            #plt.plot(f[-n:], phase[-n:], 'm-', label= 'total S21 phase')
            plt.xlabel("Frequency (Hz)")
            plt.ylabel("Phase (radians)")
            plt.legend()
            plt.show()
            """

            tau_ini = - coef_lin_ini[0] / (4 * math.pi)
            tau_fin = - coef_lin_fin[0] / (4 * math.pi)
            tau_med = (tau_ini + tau_fin) / 2

            for i in range(len(frequencies)):
                s_parameter_r = s_parameter * np.exp(2j * math.pi * (tau_med) * frequencies[i])

            if p == 0:
                if k == 0:
                    s11_phase.append(s_parameter_r)
                else:
                    s12_phase.append(s_parameter_r)
            else:
                if k == 0:
                    s21_phase.append(s_parameter_r)
                else:
                    s22_phase.append(s_parameter_r)

    return s11_phase,s21_phase,s12_phase,s22_phase,tau_med