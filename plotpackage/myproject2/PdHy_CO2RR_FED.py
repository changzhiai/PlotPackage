# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 15:14:39 2022

@author: changai
"""

#import parent dirs for local
import sys
sys.path.append("../../")

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.CO2RR import CO2RRFEDplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt
import numpy as np
from plotpackage.lib.styles import colorList
from ase.db import connect

filename = '../data/collect_vasp_PdHy.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#saved figure name
figName1 = '../pictures/CO2RR_FreeEnergy_typesetting.jpg'  #free energy diagram name
figName2 = '../pictures/ScalingRelation_typesetting.jpg' #scaling reation figure name

i = 0
fig = plt.figure(figsize=(18, 10), dpi = 300)
text = ['Single', 'Line', 'Triangle', 'Parall.', 'Island', 'Overlayer']
# col1 = [2, 2, 2, 3, 3, 5] #column in excel
# col2 = [3, 5, 4, 5, 4, 4] #column in excel
col1=2 # column in excel
col2=5 # column in excel
col1 = col1 - 2
col2 = col2 - 2
for types in ['top-new', 'line', 'triangle', 'paral-new', 'island-new', 'overly-new']:
    #change it only for excel
    sheet = types #Sheet1 by defaut
    min_row = 1 #1st column in excel
    max_row = 18 #9st column in excel
    
    ############ plot free energy diagram ###############
    stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
    #stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
    
    # # del rows; delete according to element names in excel
    del_ele = []
    # if types == 'top-new':
    #     del_ele = [] #remove distortion for near
    # if types == 'near-new':
    #     del_ele = ['Fe', 'Ru', 'Zr', 'Y', 'Mn', 'Nb', 'Zn' ] #remove distortion for near
    # elif types == 'line':
    #     del_ele = ['Ag', 'Y'] #remove distortion for line
    # elif types == 'triangle':
    #     del_ele = ['Y',] #remove distortion for triangle
    # elif types == 'paral-new':
    #     del_ele = ['Zn', 'Y', 'Zr'] #remove distortion for line
    # elif types == 'island-new':
    #     del_ele = ['Y', 'Zr', 'Sc', 'Zn'] #remove distortion for line
    # elif types == 'overly-new':
    #     del_ele = ['Sc', 'Zn', 'Y', 'Zr', 'Fe'] #remove distortion for line
    
    # if types == 'near-new':
    #     del_ele = ['Fe', 'Ru', 'Zr', 'Y', 'Mn', 'Nb', 'Zn' ] #remove distortion for near
    if types == 'top-new':
        del_ele = [] #remove distortion for near
    elif types == 'line':
        del_ele = ['Y', ] #remove distortion for line
    elif types == 'triangle':
        del_ele = ['Y',] #remove distortion for triangle
    elif types == 'paral-new':
        del_ele = ['Zn', 'Y',] #remove distortion for paral
    elif types == 'island-new':
        del_ele = ['Zn', 'Y', 'Zr'] #remove distortion for island
    elif types == 'overly-new':
        del_ele = ['Sc', 'Zn', 'Y', 'Zr', 'Fe'] #remove distortion for line
        

    del_rows = [observationName.index(each)+2 for each in del_ele]
    ### del_rows = [10, 12, 13, 18]  #delete according to rows in excel
    del_list = [x - 2 for x in del_rows]
    observationName = np.delete(observationName, del_list, 0)
    X = np.delete(X, del_list, 0)
    
    M  = 3
    ax = plt.subplot(2, 3, i + 1)
    
    descriper1 = (X[:, col1]).astype(float) 
    descriper2 = (X[:, col2]).astype(float) 
    # sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)   
    # sr.plot(ax = ax, save=False, title='', xlabel=stepsNames[col1], ylabel=stepsNames[col2], text=text[i])
    stepsNames = ['* + CO$_{2}$', 'HOCO*', 'CO*', '* + CO']  #reload step name for CO2RR
    
    CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
    CO2RRdiagram.plot(ax = ax, title='', save=False, legend=False, legendSize = 9., text = text[i], ratio=1.4)
    
    i = i +1

# for i, specis in enumerate(['Fe', 'Ru', 'Zr', 'Y', 'Mn', 'Nb', 'Zn' ]):
#     plt.hlines(0.1, 1, 2, color=colorList[specis], label= specis)
# plt.legend(fontsize=9.)
lines, labels = fig.axes[0].get_legend_handles_labels()
fig.legend(lines, labels, loc = 'lower left', ncol=9, mode="expand", borderaxespad=0.,bbox_to_anchor=(0.1, 0, 0.8, 1.02))


plt.show()
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

# CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
# #costom connection
# CO2RRdiagram.add_link(start_id=0, end_id=3)
# CO2RRdiagram.remove_link(start_id=0, end_id=1)
#CO2RRdiagram.plot(title=sheet)

# descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1
# descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4

# col1 = [2, 2, 2, 3, 3, 5] #column in excel
# col2 = [3, 5, 4, 5, 4, 4] #column in excel
# col1 = [6, 6, 6, 7, 7, 9] #column in excel
# col2 = [7, 9, 8, 9, 8, 8] #column in excel

# fig = plt.figure(figsize=(18, 16), dpi = 300)
# M  = 3
# i = 0
# for m1 in range(M-1):
#     for m2 in range(M):
#         ax = plt.subplot(M, M, m1*M + m2 + 1)
#         descriper1 = (X[:, 0]).astype(float) #step2-step1
#         descriper2 = (X[:, 1]).astype(float) #step3-step4
#         sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)
        
#         sr.plot(ax = ax, save=False, title=sheet, xlabel=stepsNames[xcol], ylabel=stepsNames[ycol])
#         i+=1
# plt.show()

#add metadata into pictures
# figNames = [figName1, figName2]
# fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
# fmd.add_metadata()