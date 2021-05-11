"""
Novel Algorithm for Resonator Parameter Extraction with Outlier Removal
by Patrick Krkotić, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O’Callaghan, 2020

Code written by Patrick Krkotić and Queralt Gallardo
patrickkrkotic@outlook.de

Developed on Python 3.7.7
"""

from numpy import *
import numpy as np
from algorithm.dBCutter import BandWidthCutterTwo



################################### BETAS - REFLECTION CIRCLE FIT ############################################

def BetaFunction(ring_slot,df,phases11_unw,phases22_unw,phase21_unw,tau,MagS21,fo_new,ql_wccfx_fo):
    
    NonScalarBetaList = []
    
    s1111 = ring_slot.s_db[:, 0, 0]
    s2222 = ring_slot.s_db[:, 1, 1]
    s2121 = ring_slot.s_db[:, 1, 0]


    s11 = 20*log10(np.sqrt(phases11_unw.real ** 2 + phases11_unw.imag**2))
    s22 = 20*log10(np.sqrt(phases22_unw.real ** 2 + phases22_unw.imag**2))
    s21 = 20*log10(np.sqrt(phase21_unw.real ** 2 + phase21_unw.imag**2))


# 1. Calculate average in 10% lower frequency range and 90% upper frequency range
    n = round(0.1 * len(df))
    #m = round(0.35 * len(df))

    s11_ini = s11[:n]  # 10% lower frequencies
    s11_fin = s11[-n:]  # 90% upper frequencies
    s11_ = np.concatenate((s11_ini, s11_fin), axis=0)

    s22_ini = s22[:n]  # 10% lower frequencies
    s22_fin = s22[-n:]  # 90% upper frequencies
    s22_ = np.concatenate((s22_ini, s22_fin), axis=0)

    s11_av_db = mean(s11_)
    s22_av_db = mean(s22_)

    # print('S11,22 ave')
    # print(s11_av_db, s22_av_db)

    s11_av = 10 ** (s11_av_db / 20)
    s22_av = 10 ** (s22_av_db / 20)

    L_in_avSC = 1 / s11_av
    L_out_avSC = 1 / s22_av
    L_s21SC = np.sqrt(L_in_avSC * L_out_avSC)

    # print('Losses SC')
    # print(L_in_avSC, L_s21SC, L_out_avSC)

    s21max = max(s21)

    sss = []
    for i in s21:
        sss.append(i)
        # print(i)
    # print(sss.index(s21max))

    s11min = s11[sss.index(s21max)]
    s22min = s22[sss.index(s21max)]

    s11mag = 10 ** (s11min / 20)
    s22mag = 10 ** (s22min / 20)
    s21mag = 10 ** (s21max / 20)

    Wbeta1SC = (1 - L_in_avSC * s11mag) / (L_in_avSC * s11mag + L_out_avSC * s22mag)
    Wbeta2SC = (1 - L_out_avSC * s22mag) / (L_in_avSC * s11mag + L_out_avSC * s22mag)

 #   Lbeta1SC = (L_s21SC * s21mag) ** 2 / (1 - (L_out_avSC * s22mag) ** 2 - (L_s21SC * s21mag) ** 2)
 #   Lbeta2SC = (L_s21SC * s21mag) ** 2 / (1 - (L_in_avSC * s11mag) ** 2 - (L_s21SC * s21mag) ** 2)

    # beta1 = (s21mag) ** 2 / (1 - (s22mag) ** 2 - (s21mag) ** 2)
    # beta2 = (s21mag) ** 2 / (1 - (s11mag) ** 2 - (s21mag) ** 2)

    # beta2New = ((1+beta1) - (2/(s21mag**2)) * beta1) + np.sqrt(((1+beta1) - (2/(s21mag**2)) * beta1)**2 - (1+beta1)**2)
    # beta2from1 = (2 * beta1 - s21mag ** 2 - beta1 * s21mag ** 2 - 2 * np.sqrt(
        # beta1 ** 2 - beta1 * s21mag ** 2 - beta1 ** 2 * s21mag ** 2)) / s21mag ** (2)

    # NonScalarBetaList.append((Lbeta1, Lbeta2))

    # print('MOFO BETA')
    # print(Lbeta1SC,Lbeta2SC)

    ################################################################### LE CIRLCE

    frequencies = df['s_db 21'].index

    deltacoupling = np.array(0.5 * ((frequencies / fo_new) - (fo_new / frequencies)))

    # [ring_slotcut11,ring_slotcut22,dfcut] = BandWidthCutterTwo(ring_slot,df)

    ringcut = np.where(ql_wccfx_fo*abs(deltacoupling) < 1/2)

    ring_slotcut11 = ring_slot.s[ringcut[0] , 0, 0]
    ring_slotcut22 = ring_slot.s[ringcut[0] , 1, 1]

    f = frequencies[ringcut[0]]
    # f = dfcut['s_db 21'].index

    s11 = ring_slotcut11
    s22 = ring_slotcut22

    s21 = phase21_unw

    dBS21 = 20 * np.log10(np.sqrt(s21.real ** 2 + s21.imag ** 2))
    s21mag = 10 ** (max(dBS21)/20)

    # # 1. Calculate average in 10% lower frequency range and 90% upper frequency range
    #
    # n = round(0.1 * len(dfcut))
    # s11_ini = s11[:n] # 10% lower frequencies
    # s11_fin = s11[-n:] # 90% upper frequencies
    # s11_ = np.concatenate((s11_ini, s11_fin), axis=0)
    #
    # s22_ini = s22[:n] # 10% lower frequencies
    # s22_fin = s22[-n:] # 90% upper frequencies
    # s22_ = np.concatenate((s22_ini, s22_fin), axis=0)
    #
    # s11_av = mean(abs(s11_))
    # s22_av = mean(abs(s22_))
    #
    # s11_avdB = mean(20 * np.log10(np.sqrt(s11_.real**2 + s11_.imag**2)))
    # s22_avdB = mean(20 * np.log10(np.sqrt(s22_.real ** 2 + s22_.imag ** 2)))
    #
    #
    # [beta1Sc, beta2Sc, s11p, s22p] = ScalarDetermination(s11, s22,s11_avdB,s22_avdB)
    #
    #
    # s11pabs = abs(s11[s11p[0][0]])
    # s22pabs = abs(s22[s22p[0][0]])
    #
    #
    # L_in_av = 1 / np.magnitude(s11_av)
    # L_out_av = 1 / np.magnitude(s22_av)
    # L_s21 = np.sqrt(L_in_av * L_out_av)
    #
    # print('Aui')
    #
    # [jbeta1,jbeta2] = ocallaghanbeta(L_in_av,L_s21,L_out_av,s11,s21mag,s22)
    #
    #
    #
    #
    # # 2. Estimate loss on input and output transmission lines based on 1.
    #
    #
    #
    # #L_in_av = np.sqrt(L_in_av.real**2 + L_in_av.imag**2)
    # #L_out_av = np.sqrt(L_out_av.real**2 + L_out_av.imag**2)

    # 3. Find the reflection coefficient gamma_r_in and gamma_r_out at resonance
    # 3.1 Find the points for which dphi/df >0 in S11 and S22


    re11= s11.real
    im11= s11.imag


    re22= s22.real
    im22= s22.imag

    numberofiterations = 0
    anchor = True


    while anchor == True: # 3.3 Otherwise, perform the circle fit of V1 and obtain gamma_r_in and gamma_r_out
        numberofiterations = numberofiterations+1
        circle_fit=True
        A11 = np.column_stack((re11, im11, np.ones(len(re11))))
        b11 = - (np.sqrt(re11 ** 2 + im11 ** 2)) ** 2
        A_plus11 = np.linalg.pinv(A11)
        x_vec11 = A_plus11.dot(b11)


        # BB = A_plus11.dot(A11)
        # ConditionNumberS11sq = np.linalg.cond(A11, 2)


        xo11 = -x_vec11[0] / 2
        yo11 = -x_vec11[1] / 2


        if ((1 / 4) * (x_vec11[0] ** 2 + x_vec11[1] ** 2)) - x_vec11[2] <= 0:
            R11 = 0
        else:
            R11 = np.sqrt(((1 / 4) * (x_vec11[0] ** 2 + x_vec11[1] ** 2)) - x_vec11[2])

        # t = np.linspace(0, 2 * np.pi, 2* len(dfcut) + 1)
        t = np.linspace(0, 2 * np.pi, 2 * len(f) + 1)
        xc11 = R11 * np.cos(t) + xo11
        yc11 = R11 * np.sin(t) + yo11

        A22 = np.column_stack((re22, im22, np.ones(len(re22))))
        b22 = - (np.sqrt(re22 ** 2 + im22 ** 2)) ** 2
        A_plus22 = np.linalg.pinv(A22)
        x_vec22 = A_plus22.dot(b22)

        CC = A_plus22.dot(A22)
        ConditionNumberS22sq = np.linalg.cond(A22, 2)


        xo22 = -x_vec22[0] / 2
        yo22 = -x_vec22[1] / 2
        if ((1 / 4) * (x_vec22[0] ** 2 + x_vec22[1] ** 2)) - x_vec22[2] <= 0:
            R22 = 0
        else:
            R22 = np.sqrt(((1 / 4) * (x_vec22[0] ** 2 + x_vec22[1] ** 2)) - x_vec22[2])

        xc22 = R22 * np.cos(t) + xo22
        yc22 = R22 * np.sin(t) + yo22

        coef11 = xo11 + 1j * yo11 - (R11 * ((xo11 + 1j * yo11) / np.sqrt(xo11 ** 2 + yo11 ** 2)))
        gamma_r_in = np.sqrt(coef11.real ** 2 + coef11.imag ** 2)

        coef22 = xo22 + 1j * yo22 - (R22 * ((xo22 + 1j * yo22) / np.sqrt(xo22 ** 2 + yo22 ** 2)))
        gamma_r_out = np.sqrt(coef22.real ** 2 + coef22.imag ** 2)

        co_11 = xo11 + yo11*1j
        co_22 = xo22 + yo22*1j

        Prover11 = []
        Prover22 = []

        s11new = []
        s22new = []

        NewIndexList = []
        NewIndexList22 = []

        for l in range(len(s11)):
            NewIndexList.append(l)

        for index in NewIndexList:
            s11new.append(s11[index])

        s11 = s11new

        for l in range(len(s22)):
            NewIndexList22.append(l)

        for index in NewIndexList22:
            s22new.append(s22[index])

        s22 = s22new

        for k in range(len(s11)):
            Prover11.append(abs(R11 - abs(s11[k] - co_11)))

        for k in range(len(s22)):
            Prover22.append(abs(R22 - abs(s22[k] - co_22)))

        condition11 = 0.1*abs(R11)
        condition22 = 0.1*abs(R22)


        if max(Prover11) > condition11:

            del s11[Prover11.index(max(Prover11))]
            re11 = np.real(s11)
            im11 = np.imag(s11)
            #print(len(Prover11))
        else:
            #print("numberofiterations S11")
            #print(numberofiterations)
            pass

        if max(Prover22) > condition22:
            del s22[Prover22.index(max(Prover22))]
            re22 = np.real(s22)
            im22 = np.imag(s22)
            #print(len(Prover22))
        else:
            #print("numberofiterations S22")
            #print(numberofiterations)
            pass

        if max(Prover11) < condition11 and max(Prover22) < condition22:
            break

    # print("Condition Number S11")
    # print(ConditionNumberS11sq)
    # print("Condition Number S22")
    # print(ConditionNumberS22sq)

    # 5. Calculate the coupling factors
    #beta1nsc = (1 - L_in_av * abs(gamma_r_in)) / (L_in_av * abs(gamma_r_in) + L_out_av * abs(gamma_r_out))
    #beta2nsc = (1 - L_out_av * abs(gamma_r_out)) / (L_in_av * abs(gamma_r_in) + L_out_av * abs(gamma_r_out))
    coef111 = xo11 + 1j * yo11 + (R11 * ((xo11 + 1j * yo11) / np.sqrt(xo11 ** 2 + yo11 ** 2)))
    coef222 = xo22 + 1j * yo22 + (R22 * ((xo22 + 1j * yo22) / np.sqrt(xo22 ** 2 + yo22 ** 2)))

    # print('Losses Circle')
    L_in_av = 1/np.abs(np.sqrt(coef111.real**2 + coef111.imag**2))
    L_out_av = 1/np.abs(np.sqrt(coef222.real**2 + coef222.imag**2))
    L_s21 = np.sqrt(L_in_av*L_out_av)

    #print(L_in_av,L_out_av)

    Lbeta1 = (L_s21 * MagS21) ** 2 / (1 - (L_out_av * abs(gamma_r_out)) ** 2 - (L_s21 * MagS21) ** 2)
    Lbeta2 = (L_s21 * MagS21) ** 2 / (1 - (L_in_av * abs(gamma_r_in)) ** 2 - (L_s21 * MagS21) ** 2)

    Wbeta1 = (1 - L_in_av * abs(gamma_r_in)) / (L_in_av * abs(gamma_r_in) + L_out_av * abs(gamma_r_out))
    Wbeta2 = (1 - L_out_av * abs(gamma_r_out)) / (L_in_av * abs(gamma_r_in) + L_out_av * abs(gamma_r_out))


    SC11 = np.abs((np.abs(co_11) - R11) / (np.abs(co_11) + R11))
    SC22 = np.abs((np.abs(co_22) - R22) / (np.abs(co_22) + R22))

    Cbeta1 = (1 - SC11) / (SC11 + SC22)
    Cbeta2 = (1 - SC22) / (SC11 + SC22)

    # print('This is Beta New Formula')
    # print('MagS21 ' + str(MagS21) )
    # print('Loss S21 ' + str(L_s21))
    # print('L_out ' + str(L_out_av))
    # print('L_in ' + str(L_in_av))
    # print('gamma ' + str(gamma_r_in) + ' ' + str(gamma_r_out))
    # print(Lbeta1,Lbeta2)



    # print('This is Beta OLD Formula')
    # print(Wbeta1,Cbeta1,Wbeta1SC)
    # print(Wbeta2, Cbeta2, Wbeta2SC)

    #betaaa.append([Lbeta1,Wbeta1,Lbeta2,Wbeta2])
    #
    # with open(
    #         'C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/FinalDataPublication/1) Couplings/Measurements/beta.dat',
    #         'w') as filetosave:
    #     filetosave.write(
    #         '\n')
    #     for fdata in betaaa:
    #         np.savetxt(filetosave, fdata, delimiter="    ", fmt='%s')
    # filetosave.close()


   # If in some rare cases, it appears a negative beta -> beta = 0.0
    #if s11pabs < abs(co_11):
    # print(abs(s11_av))
    # print(abs(co_11))
    # print(20*np.log10(s21mag))

    if 0.9 * abs(s11_av) > abs(co_11) :
   # if Lbeta1SC > 0.01:
        beta1 = Cbeta1
        # print("beta1nsc")
    else:
        beta1 = Wbeta1SC
        # print("beta1sc")

    #if s22pabs < abs(co_22):
    if 0.9 * abs(s22_av) > abs(co_22):
   # if Lbeta2SC > 0.01:
        beta2 = Cbeta2
        # print("beta2nsc")
    else:
        beta2 = Wbeta2SC
        # print("beta2sc")

    if 20*np.log10(s21mag) < -50:
        beta1 = Wbeta1SC
        beta2 = Wbeta2SC
        # print("Las dos betasc")
    # print(Wbeta1SC,Wbeta2SC)
    # print(Wbeta1,Wbeta2)

    if Wbeta1SC < 0.0 :
        beta1 = 0.0

    if Wbeta2SC < 0.0 :
        beta2 = 0.0


    #NonScalarBetaList.append((beta1,beta2))

    #NonScalarBetaList.append((Lbeta1, Lbeta2))
    # NonScalarBetaList.append((Wbeta1,Wbeta2))

    #
    # plt.figure(num=None)
    # plt.plot(re11,im11, 'yo', markersize = 10, label= 'S11 Data', zorder=1)
    # plt.plot(xc11, yc11,'-', linewidth = 3 ,label= 'S11 Fit', zorder=1)
    # plt.plot(re22, im22, 'yo', markersize = 10, label='S22 Data', zorder=1)
    # plt.plot(xc22, yc22, '-', linewidth = 3, label='S22 Fit', zorder=1)
    # plt.plot(xo11,yo11,'ro')
    # plt.plot(xo22,yo22,'ro')
    # plt.axis('equal') # otherwise circles wont be circles
    # plt.xlabel('Re(S)')
    # plt.ylabel('Im(S)')
    # plt.grid()
    # plt.legend()
    #plt.savefig(
   #     "C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/PublicationData/NEWBETATEST/" + str(beta1) + "_LSCF.png")
   #  plt.show()
   #  plt.savefig("C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/beta.png", dpi=600)
   #  plt.show()
    f = df['s_db 21'].index
    return beta1,beta2, re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, s1111, s2222, s2121

