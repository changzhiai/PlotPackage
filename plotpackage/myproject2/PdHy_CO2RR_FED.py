# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 15:14:39 2022

@author: changai
"""

import sys
sys.path.append("../..")

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.CO2RR import CO2RRFEDplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt
import numpy as np

filename = '../data/proj2/collect_vasp_PdHy.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#change it only for excel
sheet = 'CO2RR_FE' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 35 #9st column in excel

#saved figure name
figName1 = '../pictures/proj2/CO2RR_FreeEnergy_' + sheet + '.jpg'  #free energy diagram name
figName2 = '../pictures/proj2/ScalingRelation_' + sheet + '.jpg' #scaling reation figure name

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data


stepsNames = ['* + CO$_{2}$', 'HOCO*', 'CO*', '* + CO']  #reload step name for CO2RR
# observationName = ["PdH",]
CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
CO2RRdiagram.plot(title=sheet)
plt.legend(loc = "lower left", bbox_to_anchor=(0.00, -0.50, 0.8, 1.02), ncol=5, borderaxespad=0)
plt.show()


stepsNames, observationName, X = read_excel(filename, 'CO2RR_BE', 1, 5, 1, 35) #load excel data
col1 = [2, 2, 2, 3, 3, 5] #column in excel
col2 = [3, 5, 4, 5, 4, 4] #column in excel

fig = plt.figure(figsize=(18, 16), dpi = 300)
M  = 3
i = 0
for m1 in range(M-1):
    for m2 in range(M):
        ax = plt.subplot(M, M, m1*M + m2 + 1)
        xcol = col1[i] - 2 
        ycol = col2[i] - 2
        descriper1 = (X[:, xcol]).astype(float) #step2-step1
        descriper2 = (X[:, ycol]).astype(float) #step3-step4
        sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)
        
        sr.plot(ax = ax, save=False, title=sheet, xlabel=stepsNames[xcol], ylabel=stepsNames[ycol])
        i+=1
plt.show()