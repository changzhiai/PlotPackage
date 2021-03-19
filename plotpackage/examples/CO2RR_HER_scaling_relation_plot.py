# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 23:34:54 2021

@author: changai
"""

#import parent dirs for local
import sys
sys.path.append("../..")

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.CO2RR import CO2RRFEDplot
from plotpackage.lib.HER import HERFEDplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 6), dpi = 300)
ax = fig.add_subplot(111)

############CO2RR only part needs to change##############
filename = '../data/CO2RR.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#change it only for excel
sheet = 'overlayer' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 9 #9st column in excel

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
# CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
# CO2RRdiagram.plot()

descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1, *HOCO
descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4, *CO

############HER only part needs to change##############
filename2 = '../data/HER.xlsx'

#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col2 = 1 #1st column in excel
max_col2 = 4 #4th column in excel

#change it only for excel
sheet2 = 'overlayer' #Sheet1 by defaut
min_row2 = 1 #1st column in excel
max_row2 = 9 #11th column in excel

stepsNames2, observationName2, X2 = read_excel(filename2, sheet2, min_col2, max_col2, min_row2, max_row2) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
# HERdiagram = HERFEDplot(stepsNames, observationName, X, figName)
# HERdiagram.plot()

descriperHER = X2[:, 1]
#print(descriperHER)

#saved figure name
figName = '../pictures/ScalingRelation_' + sheet + '.jpg' #scaling reation figure name
sr = ScalingRelationPlot(descriper1, descriperHER, observationName2, figName)
sr.plot(save=True, xlabel='*HOCO', ylabel='*H')


# #add metadata into pictures
# figNames = [figName]
# fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
# fmd.add_metadata()
