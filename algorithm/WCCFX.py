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
    #print("Data Original " + str(len(df)))
    [ring_slotcut,dfcut,S21cut] = BandWidthCutter(ring_slot,df,S21)
    #print("Data Cutted " +str(len(dfcut)))
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


    # for mari in range(len(re21)):
    #     s21.append(20*log10(sqrt(re21[mari]*re21[mari] + im21[mari]*im21[mari])))

    # fig, ax1 = plt.subplots(figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
    # ax1.plot(np.real(s21), np.imag(s21), 'ro', markersize=12, markevery=5, label= 'S21 Data removed in % ',zorder=1)
    # ax1.plot(re21, im21, 'yo', markersize=12, markevery=5, label='S21 Data used for fit', zorder=1)
    # ax1.plot(re21b, im21b, 'go', markersize=12, markevery=5, label='S21 original', zorder=1)
    #
    # ax1.plot(re21b[0], im21b[0], 'rv', markersize=12, markevery=1, label='S21 original', zorder=1)
    # ax1.plot(re21b[-1], im21b[-1], 'rv', markersize=12, markevery=1, label='S21 original', zorder=1)
    # ax1.plot(realmove, imagmove, 'rv', markersize=12, markevery=1, label='S21 original', zorder=1)
    #
    # # ax1.plot(np.real(s21nophase), np.imag(s21nophase), 'yo', markersize=12, markevery=5, label='S21 Data No Phase Correction', zorder=1)
    # # ax1.plot(x_c, y_c, 'b', lw=4, label='S21 weigthed complex fit', zorder=1)
    # ax1.axis('equal')  # otherwise circles wont be circles
    # ax1.set_xlabel('Re(S)')
    # ax1.set_ylabel('Im(S)')
    # ax1.grid()
    # # ax1.legend(loc='center',shadow=True)
    # ax1.legend(shadow=True)
    # plt.show()

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

    conditionnumbertracker = []
    deltaecheck = []
    resfreqcheck = []
    numba = 0

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


        A21T = A21.transpose()
        ATT = np.dot(A21T,A21)
        ATTT = np.linalg.inv(ATT)
        ATTTT = np.dot(ATTT,A21T)
        x_vec21T = ATTTT.dot(b)

        # print('pseudo')
        # print(A21)
        # print('normal')
        # print(A21T)

        # print('pseudo')
        # print(x_vec21)
        # print('normal')
        # print(x_vec21T)

        # AA = A_plus21.dot(A21)
        # ConditionNumberS21sq = np.linalg.cond(A21, 2)

        # conditionnumbertracker.append(ConditionNumberS21sq)

        # nwcol1 = np.append(np.ones(len(im21)), np.zeros(len(re21)))
        # nwcol2 = np.append(np.zeros(len(im21)), np.ones(len(re21)))
        # nwcol3 = np.append(-2*delta, np.zeros(len(re21)))
        # nwcol4 = np.append(np.zeros(len(im21)), 2*delta)
        # nwcol5 = np.append(-2*im21, 2*re21)
        # nwcol6 = np.append(2*im21*delta, -2*re21*delta)
        # nwb = np.append(re21, im21)
        #
        # nwA21 = np.column_stack((nwcol1, nwcol2, nwcol3, nwcol4, nwcol5, nwcol6))
        # nwA_plus21 = np.linalg.pinv(nwA21)
        # nwx_vec21 = A_plus21.dot(nwb)
        #
        # #nwAA = nwA_plus21.dot(nwA21)
        # nwConditionNumberS21sq = np.linalg.cond(nwA21, 2)

        ql_wccfx_fo = x_vec21[5]
        # ql_wccfx_foT = x_vec21T[5]

        # print('pseudo Q')
        # print(ql_wccfx_fo)
        # print('normal Q')
        # print(ql_wccfx_foT)

        delta_e = x_vec21[4]/ql_wccfx_fo

        deltaf = fo_new * delta_e
        fo_new = fo_new + deltaf

        deltaecheck.append(delta_e)
        resfreqcheck.append(fo_new)



        # Plot Weighted Complex Circle Fit results

        C_re = x_vec21[3] / ql_wccfx_fo
        C_im = x_vec21[2] / ql_wccfx_fo
        C = complex(C_re, C_im)

        F_re = x_vec21[0]
        F_im = x_vec21[1]
        F = complex(F_re, F_im)

        G = F - C + complex(0, 2*ql_wccfx_fo*C*delta_e)

        s21_wccfx = (G/(1 + (2j * ql_wccfx_fo * (delta - delta_e))) + C)

        ## G = K and C = G in the publication

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

        # BC = 10
        BC = 10
        condis =  (BC*s21max)**(-1)

        if  max(Prover) < condis :
            #print('Approved')
            #print(max(Prover))
            #print(condis)
            Percantage = (100 - ((100 / Listlength) * len(re21)))
            #print('Removed Data ' + str(Percantage) + '%')

            # plt.plot(NumberofIterations, conditz, 'bo', label= 'Stop Condition')
            # plt.plot(NumberofIterations, maxxxxx, 'ro',label= 'Prover')
            # plt.xlabel('Number of Iteration')
            # plt.ylabel('Boundary Condition Value')
            # plt.grid()
            # plt.legend()
            # # plt.savefig(
            # #     "C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Sample Files/ADStest/" + Filename + str(BC) + "Condition.png")
            # plt.show()

            # plt.plot(NumberofIterations, lenghtsst, 'ko', label= 'Resonance Index & Final Data Length= ' + str(len(s21)))
            # plt.plot(NumberofIterations, indexxx, 'go', label= 'Index of removed Data')
            # plt.xlabel('Number of Iteration')
            # plt.ylabel('Indexvalue Normalised to Resonance')
            # plt.grid()
            # plt.legend()
            # plt.savefig(
            #     "C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Sample Files/test/Out/" + Filename + str(BC) + "Remover.png")
            # plt.show()

            break
        else:
            #TheLostOnes.append(s21[Prover.index(max(Prover))])
            #TheLostOnesFreq.append(f[Prover.index(max(Prover))])
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
    x_c = R_2 * np.cos(t) + xc
    y_c = R_2 * np.sin(t) + yc

    # # plt.plot(ring_slot.s[:,1,0].real,ring_slot.s[:,1,0].imag,'cv', markersize=10 , markevery=10, label= 'S21 Data removed in % ' + str(round(Percantage,2)), zorder=1)
    # plt.plot(np.real(TheLostOnes), np.imag(TheLostOnes), 'rv', markersize=7, markevery=2, label='S21 Data used for fit', zorder=1)
    # plt.plot(np.real(s21), np.imag(s21), 'go', markersize = 7 ,markevery=5,  label= 'S21 Data used for fit', zorder=1)
    # # plt.plot(s21_wccfx.real, s21_wccfx.imag, 'k', lw = 2.5 , label='S21 weigthed complex fit', zorder=1)
    # plt.plot(x_c, y_c, 'b', lw=2.5, label='S21 weigthed complex fit', zorder=1)
    # # plt.plot(F_re,F_im, 'ro', markersize = 15)
    # # plt.plot(G.real, G.imag, 'bo', markersize=15)
    # # plt.plot(C_re,C_im,'go',markersize=15)
    # plt.axis('equal') # otherwise circles wont be circles
    # plt.xlabel('Re(S)')
    # plt.ylabel('Im(S)')
    # plt.grid()
    # plt.legend()
    # # plt.savefig("C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Outlier.png", dpi=600)
    # # plt.savefig(
    # #     "C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Sample Files/ADStest/" + Filename + str(BC) + "Result.png")
    # plt.show()


########################################
    # font = {'size': 15}
    # plt.rc('font', **font)
    #
    # # # plt.figure()
    # # # plt.plot(resfreqcheck, 'b')
    # # # plt.xlabel('Number of Iteration')
    # # # plt.ylabel('resonance frequency [Hz]')
    # # # plt.savefig(
    # # #     "G:/Meine Ablage/200130_IEEE_MTT_Q_shared/Submission_3/Data_VNA_TEST_Copper/Streamline/Calibrated/Plotfolder/frequency_100Hz.png",
    # # #     dpi=600)
    # # # plt.show()
    # # # #
    # # plt.figure(num = None)
    # # plt.semilogy(deltaecheck, 'r', linewidth = 2, linestyle = '-')
    # # plt.xlabel('Number of Iteration')
    # # plt.ylabel('delta_e')
    # # plt.savefig("G:/Meine Ablage/200130_IEEE_MTT_Q_shared/Submission_3/Tables and Figures/delta.png", dpi=600)
    # # plt.show()
    # #
    #
    # #
    # s21nophase = ring_slotcut
    # fig, ax1 = plt.subplots(figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
    # ax1.plot(np.real(TheLostOnes), np.imag(TheLostOnes), 'rv', markersize=12, markevery=1, label= 'S21 Data removed in % ' + str(round(Percantage,2)),
    #          zorder=1)
    # ax1.plot(re21, im21, 'yo', markersize=12, markevery=5, label='S21 Fit Data', zorder=1)
    # ax1.plot(np.real(s21nophase), np.imag(s21nophase), 'go', markersize=12, markevery=5, label='S21 Original', zorder=1)
    # # ax1.plot(re21b, im21b, 'bo', markersize=12, markevery=5, label='S21 Phase Corrected', zorder=1)
    # # ax1.plot(x_c, y_c, 'b', lw=4, label='S21 weigthed complex fit', zorder=1)
    # ax1.axis('equal')  # otherwise circles wont be circles
    # ax1.set_xlabel('Re(S)')
    # ax1.set_ylabel('Im(S)')
    # ax1.grid()
    # # ax1.legend(loc='center',shadow=True)
    # ax1.legend(shadow=True)
    #
    # ax2 = plt.axes([0, 0, 1, 1])
    # # ip = InsetPosition(ax1, [0.4, 0.4, 0.25, 0.25])
    # ip = InsetPosition(ax1, [0.75, 0, 0.25, 0.25])
    # ax2.set_axes_locator(ip)
    # # mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.5')
    #
    # ax2.plot(TheLostOnesFreq,control.mag2db(TheLostOnes), 'rv', markersize=3, markevery=2, zorder=1)
    # ax2.plot(f, control.mag2db(s21), 'go', markersize=3, markevery=5,zorder=1)
    #
    #
    # ax2.tick_params(
    #     axis='both',  # changes apply to the x-axis
    #     which='both',  # both major and minor ticks are affected
    #     bottom=False,  # ticks along the bottom edge are off
    #     top=False,  # ticks along the top edge are off
    #     left=False,
    #     right = False,
    #     labelbottom=False,
    #     labelleft = False)  # labels along the bottom edge are off
    # plt.savefig("G:/Meine Ablage/200130_IEEE_MTT_Q_shared/Submission_3/Tables and Figures/Testfigure5.png", dpi=600)
    # plt.show()
##################################################
    # plt.plot(ring_slot.s[:,1,0].real,ring_slot.s[:,1,0].imag,'r-', markersize=10 , markevery=10, label= 'Original Data', zorder=1)
    # plt.plot(np.real(s21), np.imag(s21), 'go', markersize = 7 ,markevery=10,  label= 'S21 Data used for fit', zorder=1)
    # plt.plot(s21_wccfx.real, s21_wccfx.imag, 'ro', markersize=10 , label='S21 in the complex plane', zorder=1)
    # plt.plot(F_re,F_im, 'ro', markersize = 15)
    # plt.plot(G.real, G.imag, 'bo', markersize=15)
    # plt.plot(C_re,C_im,'go',markersize=15)
    # plt.axis('equal') # otherwise circles wont be circles
    # plt.xlabel('Re(S)')
    # plt.ylabel('Im(S)')
    # plt.grid()
    # plt.legend()
    # # plt.savefig("C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Example.png", dpi=600)
    # plt.show()

    # freqdata.append([fo_lf, fo_lf3p, fo_new, delta_e])
    # #
    # with open(
    #         'C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/FinalDataPublication/3) Sensitivity/SNR/Frequencies.dat',
    #         'w') as filetosave:
    #     filetosave.write(
    #         '#FileName      fl  deltae]\n')
    #     for fdata in freqdata:
    #         np.savetxt(filetosave, fdata, delimiter="\t", fmt='%s')
    # filetosave.close()
    #


    # plt.plot(conditionnumbertracker, 'ro', label='Condition Number', zorder=1)
    # # plt.axis('equal')  # otherwise circles wont be circles
    # plt.xlabel('Number of Iterations')
    # plt.ylabel('Condition Number Value')
    # plt.grid()
    # plt.legend()
    # # plt.savefig(
    # #     "C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Sample Files/ADStest/" + Filename + str(
    # #         BC) + "Result.png")
    # plt.show()

    # print("Condition Number S21")
    # print(ConditionNumberS21sq)
    # print("ConditionNumberS21sq no weitghs")
    # print(nwConditionNumberS21sq)
    # print("condtrack")
    # print(conditionnumbertracker)

    GMAG = np.sqrt(G.real**2 + G.imag**2)
    #GMAG = np.sqrt(F_re**2 + F_im**2)

    return fo_new,ql_wccfx_fo,np.real(s21), np.imag(s21),s21_wccfx.real, s21_wccfx.imag, Percantage