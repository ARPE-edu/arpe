import pandas as pd
import numpy as np
from algorithm.TheQ import Q
import matplotlib.pyplot as plt
import concurrent.futures
import os


# Helper function to wrap Q and handle exceptions
def safe_Q(file_path):
    try:
        return Q(file_path)
    except Exception as e:
        # Return some default error structure to signify failure
        return ([], [], [], [], pd.DataFrame(), [str(e)])


def TheQFuntion(filelocation):
    ListofFiles, WCCFXList, PlotDataList, Q0, Corrupt = ([] for i in range(5))
    DataToSave = pd.DataFrame()
    
    o = 0
    ListofPaths = []
    try:
        for entry in os.listdir(filelocation):
            if entry.endswith(".s2p") or entry.endswith(".S2P"):
                o += 1
                full_path = os.path.join(filelocation, entry)
                if os.path.isfile(full_path):
                    ListofPaths.append(full_path)
    except NotADirectoryError:
        if os.path.isfile(filelocation):
            ListofPaths.append(filelocation.split('/')[-1])

    # Calling Q with multiprocess using safe_Q wrapper
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.map(safe_Q, ListofPaths)

        for f in future:
            loff, wcc, plda, qq0, dts, cor = f
            [lst.extend(element)
             for lst, element
             in zip([ListofFiles, WCCFXList, PlotDataList, Q0, Corrupt],
                    [loff, wcc, plda, qq0, cor])]
            DataToSave = pd.concat([DataToSave, dts], ignore_index=True)

    return ListofFiles, WCCFXList, PlotDataList, Q0, DataToSave, Corrupt
