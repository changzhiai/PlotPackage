# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 22:26:21 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt
import numpy as np

filename = '../data/formation_energy.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 7 #5th column in excel

#change it only for excel
# sheet = 'Selectivity' #Sheet1 by defaut
sheet = 'Formation Energy' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 17 #9st column in excel

#saved figure name
figName1 = '../pictures/Formation_energy_new_' + sheet + '.jpg'  #free energy diagram name

############ plot free energy diagram ###############
colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g']
typeNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data

fig = plt.figure(figsize=(8, 6), dpi = 300)
x = np.arange(0,len(observationName),1)

marker = ['o', '^', '<', '>', 'v', 's', 'd', '.', ',', 'x', '+']
for i in range(len(typeNames)):    
    plt.plot(x, X[:,i], 's', color=colorList[i])  #plot dots
    # plt.plot(x, X[:,i], marker[i], color=colorList[i])  #plot dots
    
plt.legend(typeNames, framealpha=0.5, fontsize=12)
plt.axhline(y=0, color='r', linestyle='--')

# plt.xlim([-10, 8])
plt.ylim([-3., 2])
plt.xlabel('Doping elements', fontsize=16)
plt.ylabel('Formation energy (eV/atom)', fontsize=16)
# plt.ylabel('ΔG(HOCO*)-ΔG(H*)', fontsize=16)
# plt.title(sheet, fontsize=16)
ax = fig.gca()
ax.set_xticks(x)
ax.set_xticklabels(observationName)

ax.tick_params(labelsize=14) #tick label font size
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2) #linewith of frame
plt.show()
fig.savefig(figName1)


#add metadata into pictures
figNames = [figName1]
fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
fmd.add_metadata()