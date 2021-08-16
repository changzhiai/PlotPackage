# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 14:12:42 2021

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
from numpy import exp
from CO2toCO_acid import CO2toCO
from matplotlib import rc
# rc('font', **{'family':'sans-serif','sans-serif':['Helvetica'], 'size':8})

G_CO2g = -18.418 # eV
G_H2g = -7.096# eV
G_H2Og = -12.827 # eV
G_COg = -12.564 # eV
limiting_potenital = 0

ddG_HOCO = 0.414 # correction from binding energy to free energy
ddG_CO = 0.579


def limiting(EHOCO, ECO, T):
    """ Calculate forward rate constants and equilibrium constants 
    as function of the EO descriptor and temperature T.
    """
    
    # reaction energies
    # DE1 = EHOCO
    # DE2 = ECO - EHOCO - E_CO2g - E_H2g + E_H2Og + E_COg
    # DE3 = -ECO
    DG1 = EHOCO + ddG_HOCO
    DG2 = ECO + ddG_CO - EHOCO - ddG_HOCO - G_CO2g - G_H2g + G_H2Og + G_COg
    DG3 = -ECO - ddG_CO
    # DG3 = -0.2
    # limiting_potenital = max(DE1, DE2, DE3)
    limiting_potenital = max(DG1/(-1), DG2/(-1), DG3/(-1)) # DG3 is a fake potential because no eletron transfer

    return limiting_potenital

# EHOCO_d = {
#     "Pd": 0.42967678,
#     "Sc": -0.08249209,
#     "Ti": 0.09677125,
#     "V": 0.08057561,
#     "Mn": -0.28851255,
#     "Fe": -0.15955723,
#     "Co": 0.47024493,
#     "Ni": 0.67499474,
#     "Cu": 1.22119557,
#     # "Zn": 0.54101516,
#     # "Y": -2.76843569,
#     # "Zr": -1.44950915,
#     "Nb": 0.14885378,
#     "Mo": 0.12097152,
#     "Ru": 0.32770351,
#     "Rh": 0.53514527,
#     "Ag": 1.57118722
# }

# ECO_d = {
#     "Pd": -0.36259556,
#     "Sc": -0.53887365,
#     "Ti": -0.7954072,
#     "V": -1.07970746,
#     "Mn": -1.31038448,
#     "Fe": -1.3575169,
#     "Co": -0.90030351,
#     "Ni": -0.49399452,
#     "Cu": -0.25260203,
#     # "Zn": -0.11389156,
#     # "Y": -2.81622299,
#     # "Zr": -0.10195565,
#     "Nb": -0.94465297,
#     "Mo": -0.76108613,
#     "Ru": -1.20819791,
#     "Rh": -0.6742065,
#     "Ag": -0.09120301
# }

T = 297.15
N = 100
M = N +100
ECOs = np.linspace(-2, 0.5, N)
EHOCOs = np.linspace(-1.6, 2, M)

limit = np.empty((M,N))
for j, ECO in enumerate(ECOs):   # column
    for i, EHOCO in enumerate(EHOCOs):  # row
        limit[i][j] = limiting(EHOCO, ECO, T)


filename = '../data/binding_energy.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#saved figure name
figName1 = '../pictures/CO2RR_FreeEnergy_typesetting.jpg'  #free energy diagram name
figName2 = '../pictures/ScalingRelation_typesetting.jpg' #scaling reation figure name

index = 0
fig = plt.figure(figsize=(18, 16), dpi = 300)
text = ['Near', 'Line', 'Triangle', 'Parall.', 'Island', 'Overlayer']
# col1 = [2, 2, 2, 3, 3, 5] #column in excel
# col2 = [3, 5, 4, 5, 4, 4] #column in excel
col1=2 # column in excel
col2=3 # column in excel
col1 = col1 - 2
col2 = col2 - 2
for types in ['near-new', 'line', 'triangle', 'paral-new', 'island-new', 'overly-new']:
    #change it only for excel
    sheet = types #Sheet1 by defaut
    min_row = 1 #1st column in excel
    max_row = 18 #9st column in excel
    
    ############ plot free energy diagram ###############
    stepsNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
    #stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data
    
    # # del rows; delete according to element names in excel
    del_ele = []
    if types == 'near-new':
        del_ele = ['Fe', 'Ru', 'Zr', 'Y', 'Mn', 'Nb', 'Zn' ] #remove distortion for near
    elif types == 'line':
        del_ele = ['Ag', 'Y'] #remove distortion for line
    elif types == 'triangle':
        del_ele = ['Y',] #remove distortion for triangle
    elif types == 'paral-new':
        del_ele = ['Zn', 'Y', 'Zr'] #remove distortion for paral
    elif types == 'island-new':
        del_ele = ['Y', 'Zr',  'Zn'] #remove distortion for island
    elif types == 'overly-new':
        del_ele = ['Sc', 'Zn', 'Y', 'Zr'] #remove distortion for line
        
    del_rows = [observationName.index(each)+2 for each in del_ele]
    ### del_rows = [10, 12, 13, 18]  #delete according to rows in excel
    del_list = [x - 2 for x in del_rows]
    observationName = np.delete(observationName, del_list, 0)
    X = np.delete(X, del_list, 0)
    
    
    ax = plt.subplot(3, 3, index + 1)
    EHOCO_d = (X[:, col1]).astype(float) 
    ECO_d = (X[:, col2]).astype(float) 

    # plot contour images
    contours = np.linspace(np.min(limit), np.max(limit), 51) 
    # print(np.min(limit), np.max(limit))
    cp = ax.contourf(ECOs, EHOCOs, limit, np.round(contours, 2), cmap=plt.cm.jet_r) # X=columns, Y=rows, Z in z direction
    
    # plot scaling relation
    for i,metal in enumerate(observationName):
        plt.plot(ECO_d[i], EHOCO_d[i], 'o', color='black') 
        plt.text(ECO_d[i], EHOCO_d[i]+0.05, metal, fontsize=12, horizontalalignment='center', verticalalignment='bottom')
    
    #linear fiting and plot linear line
    m, b = np.polyfit(ECO_d, EHOCO_d, 1)
    plt.axline((ECO_d[0], ECO_d[0]*m +b), slope=m, color='black')

    plt.title(text[index])
    if index==3 or index==4 or index==5:
        plt.xlabel(r'$E_{\mathrm{CO}}$ (eV)')
    if index==0 or index==3:
        plt.ylabel(r'$E_{\mathrm{HOCO}}$ (eV)')
    if index==2:
        cbaxes = fig.add_axes([0.91, 0.659, 0.015, 0.22]) #Add position (left, bottom, width, height)
        bar = fig.colorbar(cp, cax=cbaxes)
        bar.set_label(r'Limiting potential (V)')
    if index==5:
        cbaxes = fig.add_axes([0.91, 0.391, 0.015, 0.22]) #Add position (left, bottom, width, height)
        bar = fig.colorbar(cp, cax=cbaxes)
        bar.set_label(r'Limiting potential (V)')
    
    index = index +1
    
plt.savefig('../data/limiting potential.png', dpi=300)    
plt.show()