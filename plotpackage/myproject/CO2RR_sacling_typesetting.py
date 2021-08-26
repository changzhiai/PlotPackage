# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 12:29:10 2021

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
    #saved figure name
    figName1 = './paper1/AllFreeEnergy_typesetting_{}.jpg'.format(index)  #free energy diagram name
    figName2 = './paper1/AllScalingRelation_typesetting_{}.jpg'.format(index) #scaling reation figure name
    # col1=3 # column in excel
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
        # del_ele += ['Ti', 'Sc', 'Nb', 'Zr', 'Y', 'Zn', 'V', 'Mn', 'Mo', 'Pd'] #double bond and pure
        del_rows = [observationName.index(each)+2 for each in del_ele]
        del_list = [x - 2 for x in del_rows]
        observationName = np.delete(observationName, del_list, 0)
        X = np.delete(X, del_list, 0)
           
        M  = 3
        ax = plt.subplot(3, 3, i + 1)
        descriper1 = (X[:, col1]).astype(float) 
        descriper2 = (X[:, col2]).astype(float)
            
        stepsNames = ['$E_{HOCO*}$', '$E_{CO*}$', '$E_{H*}$', '$E_{OH*}$']

        sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)   
        sr.plot(ax = ax, save=False, title='', xlabel=stepsNames[col1], ylabel=stepsNames[col2], text=text[i])
        import string
        ax.text(-0.17, 0.97, string.ascii_lowercase[i], transform=ax.transAxes, size=20, weight='bold')
        
        
        i = i +1
       
    plt.show()
    # fig.savefig(figName2)
    print('===============================')