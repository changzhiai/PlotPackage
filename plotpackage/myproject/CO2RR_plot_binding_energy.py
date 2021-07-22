# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 01:02:52 2021

@author: changai
"""
#import parent dirs for local
import sys
sys.path.append("../..")

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.CO2RR import CO2RRFEDplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt
import numpy as np

filename = '../data/binding_energy.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#change it only for excel
sheet = 'triangle' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 18 #9st column in excel

#saved figure name
figName1 = '../pictures/CO2RR_FreeEnergy_' + sheet + '.jpg'  #free energy diagram name
figName2 = '../pictures/ScalingRelation_' + sheet + '.jpg' #scaling reation figure name

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data

# # del rows
# del_rows = [5,6,7]  #rows in excel
# del_list = [x -2 for x in del_rows]
# observationName = np.delete(observationName, del_list, 0)
# X = np.delete(X, del_list, 0)

#del_rows = [10, 12, 13, 18]  #rows in excel
del_rows = []  #rows in excel
del_list = [x -2 for x in del_rows]
observationName = np.delete(observationName, del_list, 0)
X = np.delete(X, del_list, 0)

#choose some rows
# ranges = range(4,25,6)
# #ranges = [3,15,7,5]
# observationName = [observationName[i-2] for i in ranges]
# selected_rows = [i-2 for i in ranges]
# X = X[selected_rows,:]

CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
# #costom connection
# CO2RRdiagram.add_link(start_id=0, end_id=3)
# CO2RRdiagram.remove_link(start_id=0, end_id=1)
#CO2RRdiagram.plot(title=sheet)

# descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1
# descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4

col1 = 3 #column in excel
col2 = 5 #column in excel
xcol = col1 - 2 
ycol = col2 - 2
descriper1 = (X[:, xcol]).astype(float) #step2-step1
descriper2 = (X[:, ycol]).astype(float) #step3-step4
sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)
# descriper1 = (X[1::2, xcol]).astype(float) #step2-step1
# descriper2 = (X[1::2, ycol]).astype(float) #step3-step4
# sr = ScalingRelationPlot(descriper1, descriper2, observationName[1::2], figName2)
sr.plot(save=True, title=sheet, xlabel=stepsNames[xcol], ylabel=stepsNames[ycol])

#add metadata into pictures
# figNames = [figName1, figName2]
# fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
# fmd.add_metadata()

