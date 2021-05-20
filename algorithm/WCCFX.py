"""
Algorithm for Resonator Parameter Extraction from Symmetrical and Asymmetrical Transmission Responses
by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan, 2021

Code written by Queralt Gallardo and Patrick Krkotic
arpe-edu@outlook.de

Version 1.0.0
Contributors:

Developed on Python 3.7.7
"""

import skrf as rf
import control
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import curve_fit
from numpy import *
import numpy as np
import time
from algorithm.dBCutter import BandWidthCutter


def ComplexFit(ring_slot,fo_lf,df,Filename,S21):

    #######################################################
    ######## Bandwidth cutter
    #######################################################
    [ring_slotcut,dfcut,S21cut] = BandWidthCutter(ring_slot,df,S21)
    s21b = S21cut

    # S21 values from the S-Parameter Matrix in .s2p file
    re21b = s21b.real # X = REAL part of S21
    im21b = s21b.imag # Y = IMAGINARY part of S21

    # move complex circle towards origin
    realmove = abs(0.5*(re21b[0]+re21b[-1]))
    imagmove = abs(0.5*(im21b[0]+im21b[-1]))

    re21 = np.array([x-realmove for x in re21b])
    im21 = np.array([y-imagmove for y in im21b])
    s21 = np.array([z-complex(realmove,imagmove) for z in s21b])

    f = dfcut['s_db 21'].index
    delta = np.array(0.5*((f/fo_lf)-(fo_lf/f)))
    fo_new = fo_lf

    NumberofIteration = 0
    Anchor = True
    Listlength = len(re21)

    lenghtsst = []
    maxxxxx = []
    indexxx = []
    NumberofIterations = []
    conditz = []

    deltaecheck = []
    resfreqcheck = []

    while Anchor == True:
        NumberofIteration = NumberofIteration + 1
        NumberofIterations.append(NumberofIteration)
        col1 = np.append(np.ones(len(im21))*re21, np.zeros(len(re21))*im21)
        col2 = np.append(np.zeros(len(im21))*re21, np.ones(len(re21))*im21)
        col3 = np.append(-2*delta*re21, np.zeros(len(re21))*im21)
        col4 = np.append(np.zeros(len(im21))*re21, 2*delta*im21)
        col5 = np.append(-2*im21*re21, 2*re21*im21)
        col6 = np.append(2*im21*delta*re21, -2*re21*delta*im21)
        b = np.append(re21*re21, im21*im21)

        A21 = np.column_stack((col1, col2, col3, col4, col5, col6))
        A_plus21 = np.linalg.pinv(A21)
        x_vec21 = A_plus21.dot(b)

        ql_wccfx_fo = x_vec21[5]
        delta_e = x_vec21[4]/ql_wccfx_fo

        deltaf = fo_new * delta_e
        fo_new = fo_new + deltaf

        deltaecheck.append(delta_e)
        resfreqcheck.append(fo_new)


        ## G = K and C = G in the publication

        C_re = x_vec21[3] / ql_wccfx_fo
        C_im = x_vec21[2] / ql_wccfx_fo
        C = complex(C_re, C_im)

        F_re = x_vec21[0]
        F_im = x_vec21[1]
        F = complex(F_re, F_im)

        G = F - C + complex(0, 2*ql_wccfx_fo*C*delta_e)

        s21_wccfx = (G/(1 + (2j * ql_wccfx_fo * (delta - delta_e))) + C)

        NewIndexList = []
        for l in range(len(re21)):
            NewIndexList.append(l)

        s21new = []
        frequency = []

        for index in NewIndexList:
            s21new.append(s21[index])
            frequency.append(f[index])

        s21 = s21new
        f = frequency

        litst = []
        Prover = []
        for x in range(len(s21)):
            litst.append(abs(s21[x]))

        s21max = max(litst)


        for j in range(len(s21)):
            Prover.append(abs(abs(s21[j]-C)**(-1) - abs(s21_wccfx[j] - C)**(-1)))

        BC = 10
        condis =  (BC*s21max)**(-1)

        if  max(Prover) < condis :
            Percantage = (100 - ((100 / Listlength) * len(re21)))

            break
        else:
            del s21[Prover.index(max(Prover))]
            re21 = np.real(s21)
            im21 = np.imag(s21)
            del f[Prover.index(max(Prover))]
            delta = np.array(0.5 * ((f / fo_new) - (fo_new / f)))
            lenghtsst.append(0)
            maxxxxx.append(max(Prover))
            indexxx.append((Prover.index(max(Prover)) + 1 - len(s21)/2))
            NumberofIterations.append(NumberofIteration)
            conditz.append(condis)


    # Circle fitting with scipy.optimize.leastsq
    x_m = mean(s21_wccfx.real)
    y_m = mean(s21_wccfx.imag)

    def calc_R(xc, yc):  # calculate the distance of each 2D points from the center (xc, yc)
        return sqrt((s21_wccfx.real - xc) ** 2 + (s21_wccfx.imag - yc) ** 2)

    def f_2(c):  # calculate the algebraic distance between the data points and the mean circle centered at c=(xc, yc)
        Ri = calc_R(*c)
        return Ri - Ri.mean()

    center_estimate = x_m, y_m  # Find barycenter
    center_2, ier = optimize.leastsq(f_2, center_estimate)

    xc, yc = center_2  # Circle Fit center
    R_2 = calc_R(*center_2).mean()  # Circle Fit radius
    t = np.linspace(0, 2 * np.pi, len(df) + 1)
    #x_c = R_2 * np.cos(t) + xc
    #y_c = R_2 * np.sin(t) + yc

    #GMAG = np.sqrt(G.real**2 + G.imag**2)

    return fo_new,ql_wccfx_fo,np.real(s21), np.imag(s21),s21_wccfx.real, s21_wccfx.imag, Percantage