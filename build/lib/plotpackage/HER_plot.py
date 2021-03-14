# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 22:32:16 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.freeenergy import EnergyDiagram
from plotpackage.lib.HER import HERplot
import matplotlib.pyplot as plt

############only part needs to change##############
filename = './data/HER.xlsx'

#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 4 #4th column in excel

#change it only for excel
sheet = 'paral' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 11 #11th column in excel

#saved figure name
figName = './pictures/HER_FreeEnergy_' + sheet + '.jpg'  #free energy diagram name

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
HERdiagram = HERplot(stepsNames, observationName, X, figName)
HERdiagram.plot()