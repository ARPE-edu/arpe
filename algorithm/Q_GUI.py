"""
Novel Algorithm for Resonator Parameter Extraction with Outlier Removal
by Patrick Krkotić, Queralt Gallardo, Nikki Tagdulang, Montse Pont and Joan M. O’Callaghan, 2020

Code written by Patrick Krkotić and Queralt Gallardo
patrickkrkotic@outlook.de

Developed on Python 3.7.7
"""

import sys
from PyQt5 import QtWidgets,QtCore, QtGui, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtCore import QSize
import Dict
from TheQ import Q
from Dielectrics import Properties
import numpy as np


form_class = uic.loadUiType("C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Programming/TheQ/TheQ.ui")[0]


class TheQ(QtWidgets.QWidget, form_class):

    def __init__(self, parent=None):
        'This is the setup for the GUI to work with a Background'
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("The Q")
        oImage = QImage("C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Programming/TheQ/Q3.png")
        sImage = oImage.scaled(QSize(717, 717))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.show()

        self.le_files.setText("C:/Users/Kricx/OneDrive/Students/Queralt/ALBAFiles/Queralt_Gallardo/Programming/TheQ/OnlineRelaese")

        'Connections between the GUI and Python'
        self.pb_QButton.clicked.connect(self.TheQFuntion)

        self.cb_Rutile.setChecked(False)
        self.cb_Sapphire.setChecked(False)
        self.cb_Strontium.setChecked(False)
        self.Rutile = False
        self.Strontium = False
        self.Sapphire = False
        self.cb_Rutile.stateChanged.connect(self.CheckBoxFunctionR)
        self.cb_Sapphire.stateChanged.connect(self.CheckBoxFunctionS)
        self.cb_Strontium.stateChanged.connect(self.CheckBoxFunctionSt)

        self.cb_Rs.setEnabled(False)
        self.cb_Rs.setChecked(False)
        self.cb_Xs.setEnabled(False)
        self.cb_Xs.setChecked(False)
        self.SwitchRS = False
        self.SwitchXS = False
        self.cb_Rs.stateChanged.connect(self.CheckBoxFunctionRs)
        self.cb_Xs.stateChanged.connect(self.CheckBoxFunctionXs)

        'SetUp for the Plot on the GUI'
        self.graphwidget.setBackground('w')
        self.graphwidget.setLabel('left', 'IM(S21)', color='black', size=30)
        self.graphwidget.setLabel('bottom', 'RE(S21)', color='black', size=30)
        self.graphwidget.showGrid(x=True, y=True)

    'The Functions for the Checkboxes'
    def CheckBoxFunctionR(self):
        if self.cb_Rutile.isChecked() == True:
            self.Rutile = True
            self.cb_Sapphire.setEnabled(False)
            self.cb_Strontium.setEnabled(False)
            self.cb_Rs.setEnabled(True)
            self.cb_Xs.setEnabled(True)
        else:
            self.Rutile = False
            self.cb_Sapphire.setEnabled(True)
            self.cb_Strontium.setEnabled(True)
            self.cb_Rs.setEnabled(False)
            self.cb_Xs.setEnabled(False)
            self.cb_Rs.setChecked(False)
            self.cb_Xs.setChecked(False)

    def CheckBoxFunctionS(self):
        if self.cb_Sapphire.isChecked() == True:
            self.Sapphire = True
            self.cb_Rutile.setEnabled(False)
            self.cb_Strontium.setEnabled(False)
            self.cb_Rs.setEnabled(True)
            self.cb_Xs.setEnabled(True)
        else:
            self.Sapphire = False
            self.cb_Rutile.setEnabled(True)
            self.cb_Strontium.setEnabled(True)
            self.cb_Rs.setEnabled(False)
            self.cb_Xs.setEnabled(False)
            self.cb_Rs.setChecked(False)
            self.cb_Xs.setChecked(False)

    def CheckBoxFunctionSt(self):
        if self.cb_Strontium.isChecked() == True:
            self.Strontium = True
            self.cb_Rutile.setEnabled(False)
            self.cb_Sapphire.setEnabled(False)
            self.cb_Rs.setEnabled(True)
            self.cb_Xs.setEnabled(True)
        else:
            self.Strontium = False
            self.cb_Rutile.setEnabled(True)
            self.cb_Sapphire.setEnabled(True)
            self.cb_Rs.setEnabled(False)
            self.cb_Xs.setEnabled(False)
            self.cb_Rs.setChecked(False)
            self.cb_Xs.setChecked(False)

    def CheckBoxFunctionRs(self):
        self.SwitchRS = True
    def CheckBoxFunctionXs(self):
        self.SwitchXS = True


    'The Functions to plot the data'
    def plot(self, w, x, y, z,  plotname1, plotname2, colour1, colour2, Size, Symbol1 , Symbol2  , Pen):
        self.graphwidget.clear()
        if self.counter == 1:
            self.legend.scene().removeItem(self.legend)

        self.legend = self.graphwidget.addLegend(size=(120,40))
        self.graphwidget.plot(w, x, name=plotname1, pen = Pen, symbol=(Symbol1), symbolSize=Size, symbolBrush=(colour1))
        self.graphwidget.plot(y, z, name=plotname2, pen = Pen, symbol=(Symbol2), symbolSize=Size, symbolBrush=(colour2))
        self.graphwidget.autoRange()
        self.counter = + 1

    'The main start button'
    def TheQFuntion(self):

        self.TheFileLocation = self.le_files.text()
        self.NewLoc = self.TheFileLocation.replace("\\","/")
        if self.TheFileLocation == str():
            print('File Location is Missing!')

        else:
            self.pb_QButton.setEnabled(False)
            (ListofFiles,WCCFXList,PlotDataList,QUnloaded) = Q(self.NewLoc)
            self.Collector(ListofFiles,WCCFXList,PlotDataList)
            self.counter = 0

            if self.SwitchRS == False and self.SwitchXS == False:
                pass

            if self.SwitchRS == True or self.SwitchXS == True:
                self.Temperaturelist = self.le_Temperature.text()
                Dict.Temperaturelist = self.Temperaturelist
                if self.Rutile == True:

                    if self.SwitchRS == True:
                        [GFactorS,GFactorL,Epsilonr,losstang,fillingfactor]=Properties("RutileGeometricx",self.Temperaturelist)
                        print('vale')
                        self.SurfaceResistance(QUnloaded,GFactorS,GFactorL,losstang,fillingfactor)
                    else:
                        pass

                    if self.SwitchXS == True:
                        print('TRUE')
                    else:
                        pass

                elif self.Sapphire == True:
                    if self.SwitchRS == True:
                        [GFactorS, GFactorL, Epsilonr, losstang, fillingfactor] = Properties("SapphireGeometricx", self.Temperaturelist)
                        print('vale')
                        self.SurfaceResistance(QUnloaded, GFactorS, GFactorL, losstang, fillingfactor)
                    else:
                        pass

                    if self.SwitchXS == True:
                        print('TRUE')
                    else:
                        pass
                else:
                    if self.SwitchRS == True:
                        [GFactorS, GFactorL, Epsilonr, losstang,fillingfactor] = Properties("RutileGeometricx", self.Temperaturelist)
                        print('vale')
                        self.SurfaceResistance(QUnloaded, GFactorS, GFactorL, losstang,fillingfactor)
                    else:
                        pass

                    if self.SwitchXS == True:
                        print('TRUE')
                    else:
                        pass

    " Calculation of the Surface Impedance"
    def SurfaceResistance(self,QUnloaded,GFactorS,GFactorL,losstang,fillingfactor):
        if len(QUnloaded) == 1:
            self.SurfRes = 0.5*GFactorS[0]*((1/QUnloaded[0])-(0.0010/GFactorL[0])-(fillingfactor[0]*losstang[0]))

        else:
            self.SurfRes = []
            for i in range(len(QUnloaded)):
                self.SurfRes.append(0.5*GFactorS[i]*((1/QUnloaded[i])-(0.0010/GFactorL[i])-(fillingfactor[i]*losstang[i])))

        DataSave = []
        Dict.Temperaturelist = np.fromstring(Dict.Temperaturelist, dtype=float, sep=',')

        DataSave.append(np.column_stack((Dict.ListofFiles, Dict.Temperaturelist, self.SurfRes, self.SurfRes)))

        with open(Dict.basepath + '/Impedance_Results.dat', 'w') as filetosave:
            filetosave.write('#FileName   Temperature [K]   SurfaceResistance [Ohm]   SurfaceReactance [Ohm]\n')
            for data in DataSave:
                np.savetxt(filetosave, data, delimiter="    ", fmt='%s')
        filetosave.close()


    " Important for the final plot"
    def Collector(self,TheDict,TheResult,TheDATA):
        self.FilesList = QListWidget()
        self.FilesList.addItems(TheDict)
        self.FilesList.setWindowTitle("PostProcessing Plot")
        self.FilesList.setGeometry(300,300,300,600)
        self.FilesList.itemDoubleClicked.connect(self.listview_clicked)
        self.FilesList.show()
        TDict = {}
        for k in range(len(TheDict)):
            TDict[TheDict[k]] = [TheResult[k],TheDATA[k]]

        Dict.Dictionary = TDict


    def listview_clicked(self):
        itemchosen = self.FilesList.currentItem()
        Entry = Dict.Dictionary[itemchosen.text()]
        self.RedFreq = Entry[0][0]
        self.Qloaded = Entry[0][1]
        self.RS21 = Entry[1][0]
        self.IS21 = Entry[1][1]
        self.WRS21 = Entry[1][2]
        self.WIS21 = Entry[1][3]

        self.plot(self.RS21, self.IS21, self.WRS21,self.WIS21, "Measurement", "WCCF Data", "r", "b", 15, 'o', '+', None)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MyWindow = TheQ(None)
    MyWindow.show()
    app.exec_()
