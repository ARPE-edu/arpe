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

    NetworkList = []
    for touchstone in ListofFiles:
        ring_slot = rf.Network(os.path.join(basepath, touchstone))
        NetworkList.append(ring_slot)

    ###############################################################
    #### Prepare the Network Files into a Panda Dataframe
    ###############################################################

    DataFrameList = []
    for networkentry in NetworkList:
        df = networkentry.to_dataframe()
        DataFrameList.append(df)

    print("All Data Loaded")
    print("Number of elements " + str(len(ListofFiles)))

 
    ###############################################################
    #### Determination of Resonant Frequency
    ###############################################################
    print("Starting Determination of Resonant Frequency")

    for df in DataFrameList:
        ResonantFrequencyGHz.append(PeakValue(df))
        time.sleep(0.2)


    ###############################################################
    #### Determination of Delta and Complex Circle Fit
    ###############################################################

    print("Starting Weighted Complex Circle Fit")

    WCCFXList = []
    PlotDataList = []
    PercentageList = []
    for number in range(len(NetworkList)):
        [S11, S21, S12, S22, tau] = PhaseUnwrappingCorrection(NetworkList[number], DataFrameList[number])
        [fres, Ql, reals21, imags21, realwcs21, imagwcs21, Percantage] = ComplexFit(NetworkList[number],
                                                                                    ResonantFrequencyGHz[number],
                                                                                    DataFrameList[number],
                                                                                    ListofFiles[number],S21[0])
        WCCFXList.append((fres, Ql))
        PercentageList.append(Percantage)
        PlotDataListWCCFX.append((reals21, imags21, realwcs21, imagwcs21))
    

   ####################################################################################
    #### Beta Function
    ####################################################################################

    print("Starting Determination of Coupling Factors")

    for net in range(len(NetworkList)):
        
        [S11, S21, S12, S22, tau] = PhaseUnwrappingCorrection(NetworkList[net], DataFrameList[net])
        
        [b1, b2, re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List] = BetaFunction(NetworkList[net], DataFrameList[net],S11[0], S22[0], S21[0], tau, 1, WCCFXList[net][0],WCCFXList[net][1])

        couplingfactors.append((b1,b2))
        PlotDataListReflection.append((re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List))

        time.sleep(0.2)
        PlotDataList.append((PlotDataListWCCFX[net][0], PlotDataListWCCFX[net][1],PlotDataListWCCFX[net][2],PlotDataListWCCFX[net][3],PlotDataListReflection[net][0], PlotDataListReflection[net][1], PlotDataListReflection[net][2], PlotDataListReflection[net][3], PlotDataListReflection[net][4], PlotDataListReflection[net][5], PlotDataListReflection[net][6], PlotDataListReflection[net][7], PlotDataListReflection[net][8], PlotDataListReflection[net][9], PlotDataListReflection[net][10], PlotDataListReflection[net][11], PlotDataListReflection[net][12], PlotDataListReflection[net][13], PlotDataListReflection[net][14], PlotDataListReflection[net][15]))

    Q0 = []
    for value in range(len(NetworkList)):
        Q0.append(WCCFXList[value][1] * (1 + couplingfactors[value][0] + couplingfactors[value][1]))


    freq = []
    quali = []
    beta1 = []
    beta2 = []
    quali0 = []
    prozent = []

    for i in range(len(ListofFiles)):
        freq.append(WCCFXList[i][0])
        quali.append(WCCFXList[i][1])
        beta1.append(couplingfactors[i][0])
        beta2.append(couplingfactors[i][1])
        quali0.append(Q0[i])
        prozent.append(PercentageList[i])

    Data = {"Filenames": ListofFiles, "Resonant Frequency": freq, "Loaded Quality Factor": quali,
            "Coupling Factor S11": beta1, "Coupling Factor S22": beta2,
            "Unloaded Quality Factor": quali0,
            "Percentage of Data Removed": prozent}
    DataToSave = pd.DataFrame(Data)

    print('Calculations Finished')
    return ListofFiles, WCCFXList, PlotDataList, Q0, DataToSave