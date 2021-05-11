"""
Novel Algorithm for Resonator Parameter Extraction with Outlier Removal
by Patrick Krkotić, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O’Callaghan, 2020

Code written by Patrick Krkotić and Queralt Gallardo
patrickkrkotic@outlook.de

Developed on Python 3.7.7
"""
import numpy as np


def Properties(MaterialName,TemperatureList):

    Temperature = np.loadtxt(str(MaterialName) + ".txt")[:, 0]
    GeometricFactor = np.loadtxt(str(MaterialName) + ".txt")[:, 3]
    GeometricFactorLateral = np.loadtxt(str(MaterialName) + ".txt")[:, 4]
    Permittivity = np.loadtxt(str(MaterialName) + ".txt")[:, 1]
    FillingFactor = np.loadtxt(str(MaterialName) + ".txt")[:,2]
    Temploss = np.loadtxt("TanDelta.txt")[:, 0]
    LossTangent = np.loadtxt("TanDelta.txt")[:, 1]

    GS = []
    GL = []
    PE = []
    LT = []
    FF = []

    TemperatureList = np.fromstring(TemperatureList, dtype=float, sep=',')

    if len(TemperatureList) == 1:
        GS.append(np.interp(TemperatureList[0], Temperature, GeometricFactor))
        GL.append(np.interp(TemperatureList[0], Temperature, GeometricFactorLateral))
        PE.append(np.interp(TemperatureList[0], Temperature, Permittivity))
        LT.append(np.interp(TemperatureList[0], Temploss, LossTangent))
        FF.append(np.interp(TemperatureList[0], Temperature, FillingFactor))
    else:
        for Temp in TemperatureList:
            GS.append(np.interp(float(Temp), Temperature, GeometricFactor))
            GL.append(np.interp(float(Temp), Temperature, GeometricFactorLateral))
            PE.append(np.interp(float(Temp), Temperature, Permittivity))
            LT.append(np.interp(float(Temp), Temploss, LossTangent))
            FF.append(np.interp(float(Temp), Temperature, FillingFactor))

    return GS,GL,PE,LT,FF
