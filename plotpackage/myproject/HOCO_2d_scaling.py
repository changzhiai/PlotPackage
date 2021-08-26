# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 16:03:03 2021

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
# sheet = 'line-new' #Sheet1 by defaut
# min_row = 20 #1st column in excel
# max_row = 37 #9st column in excel
min_row = 1 #1st column in excel
max_row = 18 #9st column in excel

############ plot free energy diagram ###############

# types = sheet
for types in ['top-new', 'line', 'triangle', 'paral-new', 'island-new', 'overly-new']:
    sheet = types #Sheet1 by defaut
    stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
    #stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
    
    # #choose some rows
    # # selected_ele = ['Sc', 'Ti', 'V', 'Mn', 'Zn', 'Y', 'Zr', 'Nb', 'Mo'] #select according to element names in excel
    # selected_ele = ['Ti', 'Sc', 'Nb', 'Zr', 'Y', 'Zn', 'V', 'Mn', 'Mo', ] #select according to element names in excel
    selected_ele = ['Ti', 'Sc', 'Nb', 'Zr', 'Y', 'Zn', 'V', 'Mn', 'Mo'] 
    ranges = [observationName.index(each)+2 for each in selected_ele]
    observationName = [observationName[i-2] for i in ranges]
    selected_rows = [i-2 for i in ranges]
    X = X[selected_rows,:]
    
    del_ele = []
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
        del_ele = ['Sc', 'Zn', 'Y', 'Zr'] #remove distortion for line
    
    # del_ele += ['Ti', 'Sc', 'Nb', 'Zr', 'Y', 'Zn', 'V', 'Mn', 'Mo', 'Pd'] #double bond and pure
    # del_ele += ['Y', 'Cu', 'Zn', 'Ag']
    del_rows = [observationName.index(each)+2 for each in del_ele]
    ### del_rows = [10, 12, 13, 18]  #delete according to rows in excel
    del_list = [x - 2 for x in del_rows]
    observationName = np.delete(observationName, del_list, 0)
    X = np.delete(X, del_list, 0)
    
    col1=2 # HOCO*
    col2=3 # CO*
    col3=5 # OH*
    col1 = col1 - 2
    col2 = col2 - 2
    col3 = col3 - 2
    descriper1 = (X[:, col1]).astype(float) 
    descriper2 = (X[:, col2]).astype(float) 
    descriper3 = (X[:, col3]).astype(float)
    
    A = np.vstack([descriper2, descriper3]).T
    a, b = np.linalg.lstsq(A, descriper1, rcond=None)[0]
    print(a, b)
    
    _ = plt.plot(observationName, descriper1, 'o', label='Original data', markersize=10)
    _ = plt.plot(observationName, a*descriper2 + b*descriper3, 'r', label='Fitted line')
    
    # _ = plt.plot(descriper1, a*descriper2 + b*descriper3, 'o')1
    _ = plt.legend()
    _ = plt.title(types)
    plt.show()
    
