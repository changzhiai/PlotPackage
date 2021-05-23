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

filename = '../data/CO2RR.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#change it only for excel
sheet = 'overly-new' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 18 #9st column in excel

#saved figure name
figName1 = '../pictures/CO2RR_FreeEnergy_' + sheet + '.jpg'  #free energy diagram name
figName2 = '../pictures/ScalingRelation_' + sheet + '.jpg' #scaling reation figure name

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data

# # del rows; delete according to element names in excel
# del_ele = []
# del_ele = ['Ag', 'Cu', 'Ti', 'Sc'] #remove distortion for island
# del_ele += ['Sc', 'Ti', 'V', 'Mn', 'Fe', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Ru'] #del double bonds for island
# del_ele = ['Zn', 'Y', 'Zr'] #remove distortion for parallelogram
# del_ele += ['Sc', 'Ti', 'V', 'Mn', 'Zn', 'Y', 'Zr', 'Nb', 'Mo'] #del double bonds for parallelogram
del_ele = ['Sc', 'Zn', 'Y', 'Ag', 'Zr', 'Cu'] ##'Fe', 'Ni', 'Co' #remove distortion for overlayer
# del_ele += ['Sc', 'Ti', 'V', 'Mn', 'Fe', 'Co', 'Ni', 'Y', 'Zr'] #del double bonds for overlayer
del_rows = [observationName.index(each)+2 for each in del_ele]
### del_rows = [10, 12, 13, 18]  #delete according to rows in excel
del_list = [x -2 for x in del_rows]
observationName = np.delete(observationName, del_list, 0)
X = np.delete(X, del_list, 0)

#choose some rows
# # ranges = range(4,25,6) # choose one every 6 lines
# #ranges = [3,15,7,5]
# selected_ele = ['Sc', 'Ti', 'V', 'Mn', 'Zn', 'Y', 'Zr', 'Nb', 'Mo'] #select according to element names in excel
# selected_ele = ['V', 'Mn', 'Fe', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Ru'] # for island
# selected_ele = ['Sc', 'Ti', 'V', 'Mn', 'Nb', 'Mo'] #for parallelogram
# selected_ele = ['Ti', 'V', 'Mn', 'Fe', 'Co', 'Ni'] #for overlayer
# ranges = [observationName.index(each)+2 for each in selected_ele]
# observationName = [observationName[i-2] for i in ranges]
# selected_rows = [i-2 for i in ranges]
# X = X[selected_rows,:]

CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
###costom connection
# CO2RRdiagram.add_link(start_id=0, end_id=3)
# CO2RRdiagram.remove_link(start_id=0, end_id=1)
CO2RRdiagram.plot(title=sheet)


col1 = 3 #column in excel
col2 = 2 #column in excel

col3 = 4 #column in excel
col4 = 5 #column in excel

# descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1
# descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4
xcol1 = col1 - 2
xcol2 = col2 - 2
ycol1 = col3 - 2
ycol2 = col4 - 2
descriper1 = (X[:, xcol1] - X[:, xcol2]).astype(float) #step2-step1
descriper2 = (X[:, ycol1] - X[:, ycol2]).astype(float) #step3-step4
# descriper2 = (X[:, 4]).astype(float)
sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)
sr.plot(save=True, title=sheet, xlabel=stepsNames[xcol1], ylabel=stepsNames[ycol1])

#add metadata into pictures
figNames = [figName1, figName2]
fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
fmd.add_metadata()
