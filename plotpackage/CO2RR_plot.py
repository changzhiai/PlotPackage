# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 01:02:52 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.freeenergy import EnergyDiagram
from plotpackage.lib.CO2RR import CO2RRplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
import matplotlib.pyplot as plt

filename = './data/doping-top-magnetic.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#change it only for excel
sheet = 'doping-near-mag' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 9 #9st column in excel

#saved figure name
figName1 = './pictures/HER_FreeEnergy_' + sheet + '.jpg'  #free energy diagram name
figName2 = './pictures/ScalingRelation_' + sheet + '.jpg' #scaling reation figure name

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
CO2RRdiagram = CO2RRplot(stepsNames, observationName, X, figName1)
CO2RRdiagram.plot()

descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1
descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4
sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)
sr.plot()