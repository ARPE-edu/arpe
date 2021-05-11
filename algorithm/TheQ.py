
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
    PlotDataListReflection = []
    PlotDataListWCCFX = []
    TheCorrectedSparameter = []
    testoveoti = []

    

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
        ResonantFrequencyGHz.append(Lorentz(df))
        time.sleep(0.2)


    print('Resonances')
    print(ResonantFrequencyGHz)
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
        [S11, S21, S12, S22, tau] = PhaseUnwrappingCorrection(NetworkList[number], DataFrameList[number])
        AnotherBar.next()
        print(ListofFiles[number])
        [fres, Ql, reals21, imags21, realwcs21, imagwcs21, Percantage] = ComplexFit(NetworkList[number],
                                                                                    ResonantFrequencyGHz[number],
                                                                                    DataFrameList[number],
                                                                                    ListofFiles[number],S21[0])
        WCCFXList.append((fres, Ql))
        PercentageList.append(Percantage)
        PlotDataListWCCFX.append((reals21, imags21, realwcs21, imagwcs21))
    AnotherBar.finish()
    
    print(WCCFXList)

    print("Weighted Complex Circle Fit Finished")
    
   ####################################################################################
    #### Phase Corrections of DataFiles and Scalar Betas as well as new Beta Function
    ####################################################################################
    print("Starting Phase Correction")
    
    for net in range(len(NetworkList)):
        
        [S11, S21, S12, S22, tau] = PhaseUnwrappingCorrection(NetworkList[net], DataFrameList[net])
        
        #[NonScalarBetas, re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List] = BetaFunction(NetworkList[net], DataFrameList[net])
        
        
        [b1, b2, re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List] = BetaFunction(NetworkList[net], DataFrameList[net],S11[0], S22[0], S21[0], tau, 1, WCCFXList[net][0],WCCFXList[net][1])
        
        
        #PlotDataListReflection.append(BetaFunction(NetworkList[net], DataFrameList[net],S11[net], S22[net], S21[net], tau, 1))
        
        testoveoti.append((b1,b2))
        PlotDataListReflection.append((re11, im11, xc11, yc11, xo11, yo11, re22, im22, xc22, yc22, xo22, yo22, f, S1111List, S2222List, S2121List))
        
        print(testoveoti)

        time.sleep(0.2)
        PlotDataList.append((PlotDataListWCCFX[net][0], PlotDataListWCCFX[net][1],PlotDataListWCCFX[net][2],PlotDataListWCCFX[net][3],PlotDataListReflection[net][0], PlotDataListReflection[net][1], PlotDataListReflection[net][2], PlotDataListReflection[net][3], PlotDataListReflection[net][4], PlotDataListReflection[net][5], PlotDataListReflection[net][6], PlotDataListReflection[net][7], PlotDataListReflection[net][8], PlotDataListReflection[net][9], PlotDataListReflection[net][10], PlotDataListReflection[net][11], PlotDataListReflection[net][12], PlotDataListReflection[net][13], PlotDataListReflection[net][14], PlotDataListReflection[net][15]))
    print("Phase Correction Finished")

    Q0 = []
    for value in range(len(NetworkList)):
        Q0.append(WCCFXList[value][1] * (1 + testoveoti[value][0] + testoveoti[value][1]))

    
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
        beta1.append(testoveoti[i][0])
        beta2.append(testoveoti[i][1])
        quali0.append(Q0[i])
        prozent.append(PercentageList[i])

    Data = {"Filenames": ListofFiles, "Resonant Frequency": freq, "Loaded Quality Factor": quali,
            "Coupling Factor S11": beta1, "Coupling Factor S22": beta2,
            "Unloaded Quality Factor": quali0,
            "Percentage of Data Removed": prozent}

    DataToSave = pd.DataFrame(Data)

    return ListofFiles, WCCFXList, PlotDataList, Q0, DataToSave

print('BUHJHUHJHJAHJAHAAAAAA')
