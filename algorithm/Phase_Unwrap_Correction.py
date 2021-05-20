"""
Algorithm for Resonator Parameter Extraction from Symmetrical and Asymmetrical Transmission Responses
by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan, 2021

Code written by Queralt Gallardo and Patrick Krkotic
arpe-edu@outlook.de

Version 1.0.0
Contributors:

Developed on Python 3.7.7
"""

import numpy as np
import math



def PhaseUnwrappingCorrection(ring_slot,df):

    S11phase = []
    S21phase = []
    S12phase = []
    S22phase = []

#################################################
#### Define the Right Touchstone Columns
##################################################

    """
    s11 = ring_slot.s[:,0,0] # S11 values from the S-Parameter Matrix in .s2p file
    s21 = ring_slot.s[:,1,0] # S21 values from the S-Parameter Matrix in .s2p file
    s12 = ring_slot.s[:,0,1]
    s22 = ring_slot.s[:,1,1] # S22 values from the S-Parameter Matrix in .s2p file
    """

#################################################
#### Phase Unwrapping
##################################################

    f = df['s_db 21'].index

    for p in range(2):
        for k in range(2):
            ######## leads to 0 0, 0 1, 1 0 , 1 1 --> S11, S12, S21, S22

            sparamter = ring_slot.s[:,p,k] # S21 values from the S-Parameter Matrix in .s2p file
            phase = ring_slot.s_deg[:,p,k] # Phase data of S21
            phase_unw = np.zeros(len(phase))
            j = 0

            # Unwrap routine
            for i in range(len(phase_unw)):
                phase_unw[i] = math.radians(phase_unw[i]) # Degrees to radians
            for i in range(len(phase)):
                phase[i] = math.radians(phase[i]) # Degrees to radians

            disc= False
            for i in range(len(phase)-1):
                if phase[i+1] - phase[i] >= ((3*np.pi)/2) or phase[i+1] - phase[i] <= -((3*np.pi)/2): # search for phase discontinuity
                    disc= True
                    if phase[i] < phase[i+1]: # if it is a positive discontinuity
                        j = i
                        for j in range(i, len(phase)-1):
                            phase_unw[j+1] = phase[j+1] - (2*np.pi)
                    else:
                        for j in range(i, len(phase)-1):
                            phase_unw[j+1] = phase[j+1]
                elif disc==False:
                    if i ==0:
                        phase_unw[i] = phase[i]
                        phase_unw[i + 1] = phase[i + 1]
                    else:
                        phase_unw[i+1] = phase[i+1]

            n = round(0.1 * len(df))

#################################################
#### Phase Correction
##################################################

            ph_ini = phase_unw[:n] # initial 10%
            ph_fin = phase_unw[-n:] # final 10%
            for i in range(len(ph_ini)): # Degrees to radians
                ph_ini[i] = math.radians(ph_ini[i])
                ph_fin[i] = math.radians(ph_fin[i])

            # Linear regression initial part
            coef_lin_ini = np.polyfit(f[:n], ph_ini[:n], 1)
            #pol_lin_ini = np.poly1d(coef_lin_ini)

            # Linear regression final part
            coef_lin_fin = np.polyfit(f[-n:], ph_ini[-n:], 1)
            #pol_lin_fin = np.poly1d(coef_lin_fin)

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

            for i in range(len(f)):
                sparamter_r = sparamter * np.exp(2j * math.pi * (tau_med) * f[i])

            if p == 0:
                if k == 0:
                    S11phase.append(sparamter_r)
                else:
                    S12phase.append(sparamter_r)
            else:
                if k == 0:
                    S21phase.append(sparamter_r)
                else:
                    S22phase.append(sparamter_r)

    return S11phase,S21phase,S12phase,S22phase,tau_med