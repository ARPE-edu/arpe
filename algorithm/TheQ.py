"""
Algorithm for Resonator Parameter Extraction from Symmetrical and Asymmetrical Transmission Responses
by Patrick Krkotic, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O'Callaghan, 2021

Code written by Patrick Krkotic and Queralt Gallardo
arpe-edu@outlook.de

Version 1.0.0
Contributors:

Developed on Python 3.7.7
"""

import os
import skrf as rf
from algorithm.Phase_Unwrap_Correction import PhaseUnwrappingCorrection
from algorithm.PeakValueFunction import PeakValue
from algorithm.WCCFX import ComplexFit
from algorithm.final_betas import BetaFunction
import algorithm.Dict as Dict
import time
import pandas as pd


##############################################################
#### Reading Files of a Folder
##############################################################

def Q(basepath):

    ListofFiles = []
    ResonantFrequencyGHz = []
    PlotDataListReflection = []
    PlotDataListWCCFX = []
    couplingfactors = []

    NetworkList = []
    DataFrameList = []
    WCCFXList = []
    PlotDataList = []
    PercentageList = []


    Q0 = []
    freq = []
    quali = []
    beta1 = []
    beta2 = []
    quali0 = []
    prozent = []

    Corrupt = []

    o = 0
    for entry in os.listdir(basepath):
        if entry.endswith(".s2p") or entry.endswith(".S2P"):
            o += 1
            if os.path.isfile(os.path.join(basepath, entry)):
                ListofFiles.append(entry)
                print(str(o) + '. ' + entry)
    Dict.ListofFiles = ListofFiles

    ###############################################################
    #### Prepare the Files into Network Files
    ###############################################################


    for touchstone in ListofFiles:
        try:
            ring_slot = rf.Network(os.path.join(basepath, touchstone))
            #NetworkList.append(ring_slot)

        ###############################################################
        #### Prepare the Network Files into a Panda Dataframe
        ###############################################################

        #for networkentry in NetworkList:
            df = ring_slot.to_dataframe()
            #DataFrameList.append(df)

            print("All Data Loaded")
            print("Number of elements " + str(len(ListofFiles)))


        ###############################################################
        #### Determination of Resonant Frequency
        ###############################################################
            print("Starting Determination of Resonant Frequency")

        #for df in DataFrameList:
            ResonantFrequencyGHz = PeakValue(df)
            time.sleep(0.2)


        ###############################################################
        #### Determination of Delta and Complex Circle Fit
        ###############################################################

            print("Starting Weighted Complex Circle Fit")


       # for number in range(len(NetworkList)):
            [S11, S21, S12, S22, tau] = PhaseUnwrappingCorrection(ring_slot, df)
            [fres, Ql, reals21, imags21, realwcs21, imagwcs21, Percantage] = ComplexFit(ring_slot,
                                                                                        ResonantFrequencyGHz,
                                                                                        df,
                                                                                        touchstone,S21[0])
       ####################################################################################
        #### Beta Function
        ####################################################################################

            print("Starting Determination of Coupling Factors")

        #for net in range(len(NetworkList)):

            #[S11, S21, S12, S22, tau] = PhaseUnwrappingCorrection(NetworkList[net], DataFrameList[net])

            [b1, b2, re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List] = BetaFunction(ring_slot, df, S11[0], S22[0], S21[0], tau, 1, fres,Ql)

            couplingfactors.append((b1,b2))
            PlotDataListReflection.append((re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List))

            time.sleep(0.2)
            PlotDataList.append((reals21, imags21, realwcs21, imagwcs21,re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List))

    #    for value in range(len(NetworkList)):
            WCCFXList.append((fres, Ql))
            PercentageList.append(Percantage)
            PlotDataListWCCFX.append((reals21, imags21, realwcs21, imagwcs21))
            Q0.append(Ql * (1 + b1 + b2))

            print('results')
            freq.append(fres)
            quali.append(Ql)
            beta1.append(b1)
            beta2.append(b2)
            quali0.append(Ql * (1 + b1 + b2))
            prozent.append(Percantage)
            print(ListofFiles)
            # print(len(freq),len(quali),len(beta1),len(beta2),len(quali0),len(prozent))
        except:
            print("ERROR!")
            Corrupt.append(touchstone)
            continue


    print('Corrpution')
    print(Corrupt)
    print(len(ListofFiles))

    for corruptfile in Corrupt:
        ListofFiles.remove(corruptfile)

    # for i in range(len(ListofFiles)):
    #     freq.append(WCCFXList[i][0])
    #     quali.append(WCCFXList[i][1])
    #     beta1.append(couplingfactors[i][0])
    #     beta2.append(couplingfactors[i][1])
    #     quali0.append(Q0[i])
    #     prozent.append(PercentageList[i])

    print('results')
    print(ListofFiles)
    print(freq)
    print(quali)
    print(beta1)
    print(beta2)
    print(prozent)

    Data = {"Filenames": ListofFiles, "Resonant Frequency": freq, "Loaded Quality Factor": quali,
            "Coupling Factor S11": beta1, "Coupling Factor S22": beta2,
            "Unloaded Quality Factor": quali0,
            "Percentage of Data Removed": prozent}
    DataToSave = pd.DataFrame(Data)

    print('Calculations Finished')
    return ListofFiles, WCCFXList, PlotDataList, Q0, DataToSave , Corrupt