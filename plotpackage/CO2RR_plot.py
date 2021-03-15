# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 01:02:52 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.CO2RR import CO2RRFEDplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt

#plot in one picture, set this two line
fig = plt.figure(figsize=(8, 6), dpi = 300)
ax = fig.add_subplot(111)

colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g']

cases = ['overlayer', 'island', 'paral', 'doping-near-mag']
for i, sheets in enumerate(cases):
    filename = './data/doping-top-magnetic.xlsx'
    #change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
    min_col = 1 #1st column in excel
    max_col = 5 #5th column in excel
    
    #change it only for excel
    sheet = sheets #Sheet1 by defaut
    min_row = 1 #1st column in excel
    max_row = 11 #9st column in excel
    
    #saved figure name
    figName1 = './pictures/CO2RR_FreeEnergy_' + sheet + '.jpg'  #free energy diagram name
    figName2 = './pictures/ScalingRelation_' + sheet + '.jpg' #scaling reation figure name
    
    ###########################################
    #read files
    stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
    # #stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
    
    #plot free energy diagram
    # CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, figName1)
    # CO2RRdiagram.plot()
    
    # plot scaling relation between *HOCO and *CO
    descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1
    descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4
    
    sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)
    sr.plot(ax, colorList[i], colorList[i])
    
    #add metadata into pictures
    # figNames = [figName1, figName2]
    # fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
    # fmd.add_metadata()

lables = ['overlayer', 'island', 'paral', 'single atom for near site']   # reload lables 
#add legend
for specis in range(len(cases)):
    plt.hlines(0.1, 0.5, 0.5, color=colorList[specis], label= lables[specis])
plt.legend(fontsize=12)

# figure()
# title('Bejaia data')
# for c in range(C):
#     # select indices belonging to class c:
#     class_mask = y1==c
#     plot(X1[class_mask,i], X1[class_mask,j], 'o',alpha=.9)

# legend(classNames)
# xlabel(attributeNames1[i])
# ylabel(attributeNames1[j])
# # Output result to screen
# show()