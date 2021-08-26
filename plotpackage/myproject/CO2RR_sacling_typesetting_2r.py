# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 14:20:43 2021

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


# text = ['Near', 'Line', 'Triangle', 'Parall.', 'Island', 'Overlayer']
text = ['Single', 'Line', 'Triangle', 'Parall.', 'Island', 'Overlayer']
colx = [2, 2, 2, 3, 3, 5] #column in excel
coly = [3, 5, 4, 5, 4, 4] #column in excel
for index in [0, 1, 4]:
    figName1 = './paper1/AllFreeEnergy_typesetting_{}.jpg'.format(index)  #free energy diagram name
    figName2 = './paper1/AllScalingRelation_typesetting_{}.jpg'.format(index) #scaling reation figure name
    # col2=4 # column in excel
    col1=colx[index] # column in excel
    col2=coly[index] # column in excel
    col1 = col1 - 2
    col2 = col2 - 2
    i = 0
    fig = plt.figure(figsize=(18, 16), dpi = 300)
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
        #     del_ele = ['Y', 'Zr',  'Zn'] #remove distortion for line
        # elif types == 'overly-new':
        #     del_ele = ['Sc', 'Zn', 'Y', 'Zr'] #remove distortion for line
        # if types == 'near-new':
        #     del_ele = ['Fe', 'Ru', 'Zr', 'Y', 'Mn', 'Nb', 'Zn' ] #remove distortion for near
        
        # #choose some rows
        # # selected_ele = ['Sc', 'Ti', 'V', 'Mn', 'Zn', 'Y', 'Zr', 'Nb', 'Mo'] #select according to element names in excel
        # selected_ele = ['Ti', 'Sc', 'Nb', 'Zr', 'Y', 'Zn', 'V', 'Mn', 'Mo', ] #select according to element names in excel
        # ranges = [observationName.index(each)+2 for each in selected_ele]
        # observationName = [observationName[i-2] for i in ranges]
        # selected_rows = [i-2 for i in ranges]
        # X = X[selected_rows,:]
        
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
        # del_ele += ['Ti', 'Sc', 'Nb', 'Zr', 'Y', 'Zn', 'V', 'Mn', 'Mo', 'Pure'] #double bond and pure
        
         
        # dotColor = {'PdH': 'black', 'Pure': 'black', 'Pd': 'black', 'Sc': 'black', 'Ti': 'black', 'V': 'black', 
        #             'Mn': 'black', 'Fe': 'red', 'Co': 'red', 'Ni': 'red', 'Cu': 'red', 
        #             'Zn': 'black', 'Y': 'black', 'Zr': 'black', 'Nb': 'black', 'Mo': 'black', 'Ru': 'red',
        #             'Rh': 'red', 'Ag': 'red'}
        
        def delete(observationName, X, del_ele):
            del_rows = [observationName.index(each)+2 for each in del_ele]
            del_list = [x - 2 for x in del_rows]
            observationName = np.delete(observationName, del_list, 0)
            X = np.delete(X, del_list, 0)     
            descriper1 = (X[:, col1]).astype(float) 
            descriper2 = (X[:, col2]).astype(float)
            return observationName, X, descriper1, descriper2
        
        observationName1, X1, descriper11, descriper12 = delete(observationName, X, del_ele)
        
        
        # del_rows = [observationName.index(each)+2 for each in del_ele]
        # del_list = [x - 2 for x in del_rows]
        # observationName = np.delete(observationName, del_list, 0)
        # X = np.delete(X, del_list, 0)     
        # descriper1 = (X[:, col1]).astype(float) 
        # descriper2 = (X[:, col2]).astype(float)
        
        # p = 0
        # for ii, each in enumerate(observationName):
        #     if each == 'Pd':
        #         p = ii
        # observationName[p] = 'Pure'
        # np.where(observationName=='Pd', "Pure", observationName)
        
        # for ii, each in enumerate(observationName):
        #     if each == 'Pd':
        #         observationName = observationName.replace("Pd", "Pure")
        # np.char.replace(observationName, 'Pd', 'Pure')
        ax = plt.subplot(3, 3, i + 1)  
        stepsNames = ['$E_{HOCO*}$', '$E_{CO*}$', '$E_{H*}$', '$E_{OH*}$']

        sr1 = ScalingRelationPlot(descriper11, descriper12, observationName1, figName2)   
        sr1.plot(ax = ax, save=False,  dotcolor='black', linecolor='black', title='', xlabel=stepsNames[col1], ylabel=stepsNames[col2], text=text[i])
        
        
        # plot single bond
        if index == 0 or index == 1:
            del_ele += ['Ti', 'Sc', 'Nb', 'Zr', 'Y', 'Zn', 'V', 'Mn', 'Mo', 'Pure'] #double bond and pure
            observationName2, X2, descriper21, descriper22 = delete(observationName, X, del_ele)
            sr2 = ScalingRelationPlot(descriper21, descriper22, observationName2, figName2)   
            sr2.plot(ax = ax, save=False,  dotcolor='red', linecolor='red', title='', xlabel=stepsNames[col1], ylabel=stepsNames[col2], text=text[i])
        
        i = i +1
        
    plt.show()
    fig.savefig(figName2)
    print('===============================')
    
        
    
