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

# basic parameters

filename = '../data/CO2RR.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#change it only for excel
#sheet = 'Sheet1' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 11 #9st column in excel

#saved figure name
srFigName = '../pictures/multi_scaling_relation.jpg'  #free energy diagram name

colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g']
############################################

#plot in one picture, set this two line
fig = plt.figure(figsize=(8, 6), dpi = 300)
ax = fig.add_subplot(111)

sheets = ['overlayer', 'island', 'paral', 'doping-near-mag'] #plot differt sheets data in one figure
for i, sheet in enumerate(sheets):
    #read different sheets in the file
    stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
    
    # plot scaling relation between *HOCO and *CO
    descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1
    descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4
    
    sr = ScalingRelationPlot(descriper1, descriper2, observationName, srFigName)
    sr.plot(ax, colorList[i], colorList[i], False)


lables = ['overlayer', 'island', 'paral', 'single atom for near site']   # reload lables 
#add legend
for specis in range(len(sheets)):
    plt.hlines(0.1, 0.5, 0.5, color=colorList[specis], label= lables[specis])
plt.legend(fontsize=12)
plt.title('muti-sacling relation', fontsize=14)

#save figure
plt.show()
fig.savefig(srFigName)

#add metadata into picture
figNames = [srFigName]
fmd = FigsMetaData(figNames, filename, 'all', min_col, max_col, min_row, max_row)
fmd.add_metadata()
