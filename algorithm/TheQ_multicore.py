import pandas as pd
import numpy as np
from algorithm.TheQ import Q
import matplotlib.pyplot as plt
import concurrent.futures
import os


def TheQFuntion(filelocation):
    # # Return structure:
    # [ListofFiles, WCCFXList, PlotDataList, Q0, DataToSave, Corrupt] = Q(basepath)
    ListofFiles, WCCFXList, PlotDataList, Q0, Corrupt =  ([] for i in range(5))
    DataToSave=pd.DataFrame() 
    
    print('This is the filelocation' + filelocation)

    o = 0
    ListofPaths=[]
    try:
        for entry in os.listdir(filelocation):
            if entry.endswith(".s2p") or entry.endswith(".S2P"):
                o += 1
                full_path = os.path.join(filelocation,entry)
                if os.path.isfile(full_path):
                    ListofPaths.append(full_path)
                    print(str(o)+'.'+entry)
    except NotADirectoryError:
        if os.path.isfile(os.path.join(filelocation)):
            ListofPaths.append(filelocation.split('/')[-1])

    print(ListofPaths)
   
    
    # Calling Q with multiprocess
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit callables to the executor
        #for f in files:
        future = executor.map(Q,ListofPaths)
        # Retrieve the results
        for f in future:
            loff, wcc, plda, qq0, dts, cor = f
            [lst.extend(element)
                for lst,element 
                in zip([ListofFiles, WCCFXList, PlotDataList, Q0, Corrupt],
                    [loff, wcc, plda, qq0, cor])]
            DataToSave = pd.concat([DataToSave, dts], ignore_index=True)
    
    

    return ListofFiles, WCCFXList, PlotDataList, Q0, DataToSave , Corrupt