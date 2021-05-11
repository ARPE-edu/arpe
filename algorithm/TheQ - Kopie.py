
import os
import skrf as rf
from algorithm.Phase_Unwrap_Correction import PhaseUnwrappingCorrection
from algorithm.LorentzianFit import Lorentz
from algorithm.WCCFX import ComplexFit
from algorithm.final_betas import BetaFunction
import algorithm.Dict as Dict
from progress.bar import IncrementalBar
import time
import pandas as pd


##############################################################
#### Reading Files of a Folder
##############################################################

def Q(basepath):

    ListofFiles = []
    DataToSave = []
    ResonantFrequencyGHz = []

    print('Resonances')
    print(ResonantFrequencyGHz)

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

    ####################################################################################
    #### Phase Corrections of DataFiles and Scalar Betas as well as new Beta Function
    ####################################################################################
    print("Starting Phase Correction")
    PlotDataListReflection = []
    bar = IncrementalBar(max=len(NetworkList))
    for net in range(len(NetworkList)):
        [S11, S21, S12, S22, tau] = PhaseUnwrappingCorrection(NetworkList[net], DataFrameList[net])
        [NonScalarBetas, re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List] = BetaFunction(NetworkList[net], DataFrameList[net],S11[net], S22[net], S21[net], tau, 1)
        PlotDataListReflection.append((re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List))
        bar.next()
        time.sleep(0.2)
    bar.finish()

    print("Phase Correction Finished")

    ###############################################################
    #### Determination of Resonant Frequency
    ###############################################################
    print("Starting Determination of Resonant Frequency")
    TheBar = IncrementalBar(max=len(NetworkList))
    for df in DataFrameList:
        ResonantFrequency = Lorentz(df)
        TheBar.next()
        time.sleep(0.2)
    TheBar.finish()

    for frequency in ResonantFrequency:
        ResonantFrequencyGHz.append(frequency / 10 ** 9)

    print("Determination of Resonant Frequency Finished")

    ###############################################################
    #### Determination of Delta and Complex Circle Fit
    ###############################################################

    print("Starting Weighted Complex Circle Fit")

    WCCFXList = []
    PlotDataList = []
    AnotherBar = IncrementalBar(max=len(NetworkList))
    PercentageList = []
    for number in range(len(NetworkList)):
        AnotherBar.next()
        print(ListofFiles[number])
        [fres, Ql, reals21, imags21, realwcs21, imagwcs21, Percantage] = ComplexFit(NetworkList[number],
                                                                                    ResonantFrequency[number],
                                                                                    DataFrameList[number],
                                                                                    ListofFiles[number])
        WCCFXList.append((fres, Ql))
        PlotDataList.append((reals21, imags21, realwcs21, imagwcs21, PlotDataListReflection[number][0], PlotDataListReflection[number][1], PlotDataListReflection[number][2], PlotDataListReflection[number][3], PlotDataListReflection[number][4], PlotDataListReflection[number][5], PlotDataListReflection[number][6], PlotDataListReflection[number][7], PlotDataListReflection[number][8], PlotDataListReflection[number][9], PlotDataListReflection[number][10], PlotDataListReflection[number][11], PlotDataListReflection[number][12], PlotDataListReflection[number][13], PlotDataListReflection[number][14], PlotDataListReflection[number][15]))
        PercentageList.append(Percantage)
    AnotherBar.finish()


    print("Weighted Complex Circle Fit Finished")

    Q0 = []
    for value in range(len(NetworkList)):
        Q0.append(WCCFXList[value][1] * (1 + NonScalarBetas[value][0] + NonScalarBetas[value][1]))

    ###############################################################
    #### Prepare the Data to be stored in a file
    ###############################################################
    #
    # DataToSave.append(
    #     np.column_stack(
    #         (
    #             ListofFiles,
    #             WCCFXList,
    #             NonScalarBetas,
    #             Q0,PercentageList
    #         )
    #     )
    # )
    freq = []
    quali = []
    beta1 = []
    beta2 = []
    quali0 = []
    prozent = []

    for i in range(len(ListofFiles)):
        freq.append(WCCFXList[i][0])
        quali.append(WCCFXList[i][1])
        beta1.append(NonScalarBetas[i][0])
        beta2.append(NonScalarBetas[i][1])
        quali0.append(Q0[i])
        prozent.append(PercentageList[i])

    Data = {"Filenames": ListofFiles, "Resonant Frequency": freq, "Loaded Quality Factor": quali,
            "Coupling Factor S11": beta1, "Coupling Factor S22": beta2,
            "Unloaded Quality Factor": quali0,
            "Percentage of Data Removed": prozent}

    DataToSave = pd.DataFrame(Data)

    return ListofFiles, WCCFXList, PlotDataList, Q0, DataToSave

