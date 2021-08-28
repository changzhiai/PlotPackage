# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 22:32:16 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.HER import HERFEDplot
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt

############only part needs to change##############
filename = '../data/HER.xlsx'

#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 4 #4th column in excel

#change it only for excel
sheet = 'top-new' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 11 #11th column in excel

#saved figure name
figName = '../pictures/HER_FreeEnergy_' + sheet + '.jpg'  #free energy diagram name

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data



#choose some rows
# # ranges = range(4,25,6) # choose one every 6 lines
# #ranges = [3,15,7,5]
# selected_ele = ['Sc', 'Ti', 'V', 'Mn', 'Zn', 'Y', 'Zr', 'Nb', 'Mo'] #select according to element names in excel
# selected_ele = ['V', 'Mn', 'Fe', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Ru'] # for island
# selected_ele = ['Sc', 'Ti', 'V', 'Mn', 'Nb', 'Mo'] #for parallelogram
# selected_ele = ['Ti', 'V', 'Mn', 'Fe', 'Co', 'Ni'] #for overlayer
selected_ele = ['Pure']
ranges = [observationName.index(each)+2 for each in selected_ele]
observationName = [observationName[i-2] for i in ranges]
selected_rows = [i-2 for i in ranges]
X = X[selected_rows,:]


stepsNames = ['* + $H^{+}$', 'H*', '* + $1/2H_{2}$']  #reload step name for CO2RR
observationName = ["PdH",]

HERdiagram = HERFEDplot(stepsNames, observationName, X, figName)
HERdiagram.plot(title=sheet)

#add metadata into pictures
figNames = [figName]
fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
fmd.add_metadata()
