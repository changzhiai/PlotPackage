# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:59:23 2021

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

kB = 8.617e-5 # Boltzmann constant in eV/K
hplanck = 4.135669e-15 # eV s
T0 = 297.15
# T0 = 370
Gact0 = Gact1 = Gact2 = 0.475 # activative free energy
tc0 = tc1 = tc2 = 0.5  #???
A_act1 = np.exp( - Gact1 / ( kB * T0 ) ) # 
A_act2 = np.exp( - Gact2 / ( kB * T0 ) ) # electrochemical prefactor, fitting
G_1act_cap = -Gact1
G_2act_cap = -Gact2

nu_e = kB * T0 / hplanck
nu_c = 1.e13

cHp0 = 10.**(-0.)
UHER0 = URHE0 = kB * T0 * np.log(cHp0)   # introduced to shift the plotted potential window to the relevant range w

U0 = -0.4 # applied potential vs. she
U = U0 + UHER0

ddG_HOCO = 0.414 # correction from binding energy to free energy
ddG_CO = 0.579

def get_K1(E_HOCO, U, T=T0):
    """ K1 using HOCO binding
    """
    beta = 1. / (kB * T) 
    dG = E_HOCO + ddG_HOCO
    K1 = exp( - (dG + 1.0 * U ) * beta )
    return K1

def get_K2(E_HOCO, E_CO, U,  T=T0):
    """ K2 using HOCO and CO binding.
    """
    beta = 1. / (kB * T) 
    dG = E_CO + ddG_CO - E_HOCO - ddG_HOCO - G_CO2g - G_H2g + G_H2Og + G_COg
    K2 =  exp( - ( dG + 1.0 * U ) * beta ) 
    return K2

def get_K3(E_CO, U, T=T0):
    """ K3 asumming scaling.
    """
    beta = 1. / (kB * T) 
    dG = - (E_CO + ddG_CO)
    K3 = exp( - dG * beta )
    return K3



def get_k1(nu, E_HOCO, U, T=T0, tc=tc1):
    """ k1 using HOCO binding (vs CO2 and H2)
    """
    beta = 1. / (kB * T) 
    dG_rhe = E_HOCO + ddG_HOCO # vs. RHE
    Urev_rhe = -dG_rhe
    # dG_she = dG_rhe 
    # Urev_she = -dG_she + UHER0
    k1 = nu * A_act1 * exp( - max( ( U - Urev_rhe ) * tc, G_1act_cap) * beta ) 
    #k1 = nu * A_act1 * exp( - min( ( U - dG_she ) * tc, 0) * beta ) 
    #dGw =  - kB * T * np.log(Kw)
    #dG = 0. * Gact0 + ddG_HOCO + E_HOCO + dGw
    #U0 = (1./tc - 1.) * dG - Gact0
    #k1 = nu * A_act1 * exp( - max( dG + ( U - U0 ) * tc, 0) * beta )
    return k1

def get_k2(nu, E_HOCO, E_CO, U, T=T0, tc=tc2):
    """ k2 using HOCO and CO energies.
    """    
    beta = 1. / (kB * T)  
    dG_rhe = E_CO + ddG_CO - E_HOCO - ddG_HOCO - G_CO2g - G_H2g + G_H2Og + G_COg
    Urev_rhe = -dG_rhe
    # dG_she = dG_rhe
    # Urev_she = - dG_she + URHE0
    k2 = nu * A_act2 * exp( - max(( U - Urev_rhe ) * tc, G_2act_cap) * beta ) 
    return k2

def get_k3(nu, E_CO, U, T=T0, tc=tc0):
    """ k3 assuming scaling.
    """
    beta = 1. / (kB * T) 
    dE = - E_CO
    dE = max(dE,0)
    k3 = nu * exp( - dE * beta )
    return k3


def get_rates(nu_e, nu_c, E_HOCO, E_CO, U, T=T0):
    """ Returns rate constants and equilibirum constants,
    """
    K1 = get_K1(E_HOCO, U, T=T)
    K2 = get_K2(E_HOCO, E_CO, U, T=T)
    K3 = get_K3(E_CO, U, T=T)
    k1 = get_k1(nu_e, E_HOCO, U, T=T)
    k2 = get_k2(nu_e, E_HOCO, E_CO, U, T=T)
    k3 = get_k3(nu_c, E_CO, U, T=T)
    return k1, K1, k2, K2, k3, K3

# ECO_d = {
#     "Pd": -0.36259556,
#     # "Sc": -0.53887365,
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


# EHOCO_d = {
#     "Pd": 0.42967678,
#     # "Sc": -0.08249209,
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

pCO2 = 1.
pCO =  1.
xH2O = 1.
cHp = cHp0 #1.
# N = 20*4
# M = 30*4
N = 20*4
M = 20*4
R = np.empty([M,N])
Thetas = np.empty([M,N,3])
# E_HOCO_e = np.linspace(-0.8, 1.45, M)
# E_CO_e = np.linspace(-2.2, 0.6, N)
E_CO_e = np.linspace(-1.8, 1., N)
E_HOCO_e = np.linspace(-1.2, 1.8, M)

jmax = 10.0e3 # exptl current plateau's at 10 mA/cm2 
jmin = 0.1
for j, E_CO in enumerate(E_CO_e):
    for i, E_HOCO in enumerate(E_HOCO_e):
        k1, K1, k2, K2, k3, K3 = get_rates(nu_e, nu_c, E_HOCO, E_CO, U, T=T0)
        rm = CO2toCO(pCO2, pCO, xH2O, cHp, k1, K1, k2, K2, k3, K3)
        # rm = CO2toCO(pCO2, pCO, xH2O, cOHm, k1, K1, k2, K2, k3, K3, T0)
        thetas, rates = rm.solve()
        print(rates)
        rate = min(jmax, rates[0])
        rate = max(jmin, rate)
        R[i,j] = np.log10(rate)
        Thetas[i,j,:] = thetas

filename = '../data/binding_energy.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 5 #5th column in excel

#saved figure name
figName1 = '../pictures/CO2RR_FreeEnergy_typesetting.jpg'  #free energy diagram name
figName2 = '../pictures/ScalingRelation_typesetting.jpg' #scaling reation figure name

index = 0
fig = plt.figure(figsize=(18, 16), dpi = 300)
text = ['Single', 'Line', 'Triangle', 'Parall.', 'Island', 'Overlayer']
# col1 = [2, 2, 2, 3, 3, 5] #column in excel
# col2 = [3, 5, 4, 5, 4, 4] #column in excel
col1=2 # column in excel
col2=3 # column in excel
col1 = col1 - 2
col2 = col2 - 2
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
    # if types == 'near-new':
    #     del_ele = ['Fe', 'Ru', 'Zr', 'Y', 'Mn', 'Nb', 'Zn' ] #remove distortion for near
    # if types == 'top-new':
    #     del_ele = [] #remove distortion for near
    # elif types == 'line':
    #     del_ele = ['Ag', 'Y'] #remove distortion for line
    # elif types == 'triangle':
    #     del_ele = ['Y',] #remove distortion for triangle
    # elif types == 'paral-new':
    #     del_ele = ['Zn', 'Y', 'Zr'] #remove distortion for paral
    # elif types == 'island-new':
    #     del_ele = ['Y', 'Zr',  'Zn'] #remove distortion for island
    # elif types == 'overly-new':
    #     del_ele = ['Sc', 'Zn', 'Y', 'Zr'] #remove distortion for line
    # if types == 'near-new':
    #     del_ele = ['Fe', 'Ru', 'Zr', 'Y', 'Mn', 'Nb', 'Zn' ] #remove distortion for near
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
        
    del_rows = [observationName.index(each)+2 for each in del_ele]
    ### del_rows = [10, 12, 13, 18]  #delete according to rows in excel
    del_list = [x - 2 for x in del_rows]
    observationName = np.delete(observationName, del_list, 0)
    X = np.delete(X, del_list, 0)
    
    M  = 3
    ax = plt.subplot(3, 3, index + 1)
    EHOCO_d = (X[:, col1]).astype(float) 
    ECO_d = (X[:, col2]).astype(float) 
    # sr = ScalingRelationPlot(descriper1, descriper2, observationName, figName2)   
    # sr.plot(ax = ax, save=False, title='', xlabel=stepsNames[col1], ylabel=stepsNames[col2], text=text[index])
    
    contours = np.linspace(np.log10(jmin), np.log10(jmax), 11) 
    plt.contourf(E_CO_e, E_HOCO_e, R, contours, cmap=plt.cm.jet)
    for i,metal in enumerate(observationName):
        plt.plot(ECO_d[i], EHOCO_d[i], 'o', color='white') 
        plt.text(ECO_d[i], EHOCO_d[i]+0.05, metal, fontsize=12, horizontalalignment='center', verticalalignment='bottom', color='white')
    
    #linear fiting and plot linear line
    # m, b = np.polyfit(ECO_d, EHOCO_d, 1)
    # plt.axline((ECO_d[3], ECO_d[3]*m +b), slope=m, color='white')
    m, b = np.polyfit(EHOCO_d, ECO_d, 1)
    plt.axline(( ECO_d[0], ECO_d[0]/m-b/m), slope=1/m, color='white')
    # plt.plot(self.descriper1, m * self.descriper1 + b, linewidth=2, color=linecolor)
        
    plt.xlim([E_CO_e[0]+0.1, E_CO_e[-1]-0.1])
    plt.ylim([E_HOCO_e[0]+0.1, E_HOCO_e[-1]-0.1])
    ax.tick_params(labelsize=12) #tick label font size
    # plt.title(text[index], fontsize=14,)
    plt.text(0.05, 0.93, text[index], horizontalalignment='left', verticalalignment='center', transform=ax.transAxes, fontsize=14, color='white', fontweight='bold')        
    # if index==2 or index==5:
    #     bar = plt.colorbar(ticks=np.arange(min(contours), max(contours), 0.5))
    #     bar.set_label(r'log$_{10}$(j/$\mu$Acm$^{-2}$)')
    if index==3 or index==4 or index==5:
        plt.xlabel(r'$E_{\mathrm{CO}}$ (eV)', fontsize=14,)
    if index==0 or index==3:
        plt.ylabel(r'$E_{\mathrm{HOCO}}$ (eV)', fontsize=14,)
    if index==2:
        cbaxes = fig.add_axes([0.91, 0.659, 0.015, 0.22]) #Add position (left, bottom, width, height)
        bar = plt.colorbar(ticks=np.arange(min(contours), max(contours), 0.5), cax=cbaxes)
        bar.ax.tick_params(labelsize=10)
        bar.set_label(r'log$_{10}$(j/$\mu$Acm$^{-2}$)', fontsize=14,)
    if index==5:
        cbaxes = fig.add_axes([0.91, 0.391, 0.015, 0.22]) #Add position (left, bottom, width, height)
        bar = plt.colorbar(ticks=np.arange(min(contours), max(contours), 0.5), cax=cbaxes)
        bar.ax.tick_params(labelsize=12)
        bar.set_label(r'log$_{10}$(j/$\mu$Acm$^{-2}$)', fontsize=14,)
    
    index = index +1
    
plt.savefig('../data/CO2toCO_rate_vs_HOCO_CO.png', dpi=300)    
plt.show()










