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
max_col = 2 #5th column in excel

#change it only for excel
sheet = 'Sheet1' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 7 #9st column in excel

#saved figure name
figName1 = '../pictures/Formation_energy_' + sheet + '.jpg'  #free energy diagram name

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data

fig = plt.figure(figsize=(8, 6), dpi = 300)
x = np.arange(0,len(observationName),1)
plt.plot(x, X[:,0], 's', color='k')  #plot dots
plt.axhline(y=0, color='r', linestyle='--')

# plt.xlim([-10, 8])
plt.ylim([-1, 1])
plt.xlabel('Doping elements', fontsize=14)
plt.ylabel('Formation energy (eV/atom)', fontsize=14)
ax = fig.gca()
ax.set_xticks(x)
ax.set_xticklabels(observationName)

ax.tick_params(labelsize=12) #tick label font size
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2) #linewith of frame
plt.show()
plt.savefig(figName1)


#add metadata into pictures
figNames = [figName1]
fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
fmd.add_metadata()