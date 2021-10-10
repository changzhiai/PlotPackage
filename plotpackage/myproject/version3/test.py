# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 18:47:53 2021

@author: changai
"""

import sys
sys.path.append("../../..")

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.CO2RR import CO2RRFEDplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt
import numpy as np

filename = './sites.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1+18 #1st column in excel
max_col = 5+18 #5th column in excel

#saved figure name
figName1 = './paper1/All_FreeEnergy_typesetting.jpg'  #free energy diagram name
# figName2 = './paper1//ScalingRelation_typesetting.jpg' #scaling reation figure name

i = 0
fig = plt.figure(figsize=(18, 10), dpi = 300)
text = ['Single', 'Dimer', 'Triangle', 'Parall.', 'Island', 'Overlayer']
# col1 = [2, 2, 2, 3, 3, 5] #column in excel
# col2 = [3, 5, 4, 5, 4, 4] #column in excel
# col1=2 # column in excel
# col2=5 # column in excel
# col1 = col1 - 2
# col2 = col2 - 2
for types in ['single_b', 'dimer_b', 'triangle_b', 'paral_b', 'island_b', 'overly_b']:
    #change it only for excel
    sheet = types #Sheet1 by defaut
    min_row = 1+1 #1st column in excel
    max_row = 24+1 #9st column in excel
    
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
    if types == 'single_b':
            del_ele = [] #remove distortion for near
    elif types == 'dimer_b':
        del_ele = ['Y', ] #remove distortion for line
    elif types == 'triangle_b':
        del_ele = ['Y',] #remove distortion for triangle
    elif types == 'paral_b':
        del_ele = ['Zn', 'Y', 'Cd'] #remove distortion for paral
    elif types == 'island_b':
        del_ele = ['Zn', 'Y', 'Zr', 'Hf', 'Cd'] #remove distortion for island
    elif types == 'overly_b':
        del_ele = ['Sc', 'Zn', 'Y', 'Zr', 'Hf', 'Cd'] #remove distortion for line
        

    del_rows = [observationName.index(each)+2 for each in del_ele]
    ### del_rows = [10, 12, 13, 18]  #delete according to rows in excel
    del_list = [x - 2 for x in del_rows]
    observationName = np.delete(observationName, del_list, 0)
    X = np.delete(X, del_list, 0)
    
    M  = 3
    ax = plt.subplot(2, 3, i + 1)
    
#     descriper1 = (X[:, col1]).astype(float) 
#     descriper2 = (X[:, col2]).astype(float) 
    # sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)   
    # sr.plot(ax = ax, save=False, title='', xlabel=stepsNames[col1], ylabel=stepsNames[col2], text=text[i])
    stepsNames = ['* + CO$_{2}$', 'HOCO*', 'CO*', '* + CO']  #reload step name for CO2RR
    
    CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
    CO2RRdiagram.plot(ax = ax, title='', save=False, legendSize = 9., text = text[i], ratio=1.3, legend=False, ymin=-1.7, ymax=1.9) # set ymin and ymax if using fixed y range
    
    # plt.xlim(1/2*xmin/scale, (xmax-1/2*xmin)/scale)
    # plt.xlim(0/scale, (xmax-xmin)/scale)
    # plt.ylim(-1.7, 1.9)
    
    import string
    ax.text(-0.17, 0.97, string.ascii_lowercase[i], transform=ax.transAxes, size=20, weight='bold')
    
    i = i +1

lines, labels = fig.axes[0].get_legend_handles_labels()
fig.legend(lines, labels, loc = 'lower left', ncol=9, mode="expand", borderaxespad=0.,bbox_to_anchor=(0.1, -0.04, 0.8, 1.02), fontsize=14,edgecolor='grey' )
plt.show()

fig.savefig(figName1, dpi=300, bbox_inches='tight')