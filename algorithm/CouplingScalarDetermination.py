import pylab
import control
import numpy as np
from colorama import Fore, Back, Style



def ScalarDetermination(df):
    ##################################### BETAS - SCALAR MEASUREMENT ##############################################
    ScalarBetaList = []
    # Values without gaps at f0
    s11 = df['s_db 11'].min() - df['s_db 11'].values[0]
    s22 = df['s_db 22'].min() - df['s_db 22'].values[0]

    # S-values from dB to lineal
    s11 = control.db2mag(s11)
    s22 = control.db2mag(s22)

    # Find betas -> beta = coupling factor
    beta1 = (1 - np.absolute(s11))/(np.absolute(s11) + np.absolute(s22)) # beta1 = (1-|S11|)/(|S11|+|S22|)
    beta2 = (1 - np.absolute(s22))/(np.absolute(s11) + np.absolute(s22)) # beta2 = (1-|S22|)/(|S11|+|S22|)

    ScalarBetaList.append((beta1,beta2))

    return ScalarBetaList
