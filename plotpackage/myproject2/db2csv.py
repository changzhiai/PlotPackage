# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 13:55:28 2022

@author: changai
"""
import sys
sys.path.append("../..")

from ase.db import connect
import pandas as pd
from plotpackage.lib.io import read_excel
from plotpackage.lib.CO2RR import CO2RRFEDplot
from plotpackage.lib.scalingrelation import ScalingRelationPlot
import matplotlib.pyplot as plt
from styleframe import StyleFrame, Styler
import numpy as np

def db2xls(system_name, xls_name, db, sheet_free_energy, sheet_binding_energy):
    """
    convert database into excel
    
    totally produce four sheets
    """
    E_H2g = -7.158 # eV
    E_CO2g = -18.459
    E_H2Og = -12.833
    E_COg = -12.118
    
    # G_gas = E_pot + E_ZPE + C_Idel_gas - TS + Ecorr_overbing + E_solvent
    G_H2g = E_H2g + 0.274	+ 0.091 - 0.403 + 0.1 + 0
    G_CO2g = E_CO2g + 0.306 + 0.099 - 0.664 + 0.3 + 0
    G_H2Og = E_H2Og + 0.572 + 0.104 - 0.670
    G_COg = E_COg + 0.132 + 0.091 - 0.669
    
    # G_gas = E_ZPE + C_harm - TS + Ecorr_overbing + E_solvent
    Gcor_H = 0.190 + 0.003 - 0.004 + 0 + 0
    Gcor_HOCO = 0.657 + 0.091 - 0.162 + 0.15 - 0.25
    Gcor_CO = 0.186 + 0.080 - 0.156 + 0 - 0.10
    Gcor_OH = 0.355 + 0.056 - 0.103
    
    ids = []
    formulas = []
    sites = []
    adsors = []
    energies = []
    for row in db.select():
        uniqueid = row.uniqueid
        items = uniqueid.split('_')
        id = items[0]
        formula = items[1]
        i_X = formula.find('X')
        formula = formula[:i_X] + formula[i_X+4:] # remove Xxxx
        site = items[2]
        adsor = items[3]
        
        ids.append(id)
        formulas.append(formula)
        sites.append(site)
        adsors.append(adsor)
        energies.append(row.energy)
    
    tuples = {'Id': ids,
              'Surface': formulas,
              'Site': sites,
              'Adsorbate': adsors,
              'Energy': energies,
             }
    df = pd.DataFrame(tuples)
    
    """
    Save the original data and sorted by adsorbate
    """
    uniqueids = df['Id'].astype(int).unique()
    df_sort  = pd.DataFrame()
    custom_dict = {'surface':0, 'HOCO': 1, 'CO': 2, 'H': 3, 'OH':4} 
    for id in uniqueids:
        df_sub = df.loc[df['Id'].astype(int) == id]
        df_sub = df_sub.sort_values(by=['Adsorbate'], key=lambda x: x.map(custom_dict))
        
        Surface = df_sub.loc[df_sub['Adsorbate'] == 'surface']
        E_Surface = Surface.Energy.values[0]
        
        Binding_energy = []
        for i,row in df_sub.iterrows():
            ads = row['Adsorbate']
            if ads == 'surface':
                Binding_energy.append(0)
            elif ads == 'HOCO':
                E_HOCO = row.Energy
                Eb_HOCO = E_HOCO - E_Surface - E_CO2g - 0.5 * E_H2g
                Binding_energy.append(Eb_HOCO)
            elif ads == 'CO':
                E_CO = row.Energy
                Eb_CO = E_CO - E_Surface - E_COg
                Binding_energy.append(Eb_CO)
            elif ads == 'H':
                E_H = row.Energy
                Eb_H = E_H - E_Surface - 0.5 * E_H2g
                Binding_energy.append(Eb_H)
            elif ads == 'OH':
                E_OH = row.Energy
                Eb_OH = E_OH - E_Surface - E_H2Og + 0.5 * E_H2g
                Binding_energy.append(Eb_OH)
                
        df_sub['BE'] = Binding_energy
        df_sort = df_sort.append(df_sub, ignore_index=True)
    df_sort.to_excel(xls_name, sheet_name='Origin', float_format='%.3f')
    
    surfaces = []
    step_ini = []
    step_HOCO = []
    step_CO = []
    step_final = []
    Eb_HOCOs = []
    Eb_COs = []
    Eb_Hs = []
    Eb_OHs = []
    FE_final = G_COg + G_H2Og - G_CO2g - G_H2g
    df_new  = pd.DataFrame()
    for id in uniqueids:
        # print(id)
        df_sub = df.loc[df['Id'].astype(int) == id]
        Surface = df_sub.loc[df_sub['Adsorbate'] == 'surface']
        E_Surface = Surface.Energy.values[0]
        # print(df_sub)
        HOCOs = df_sub.loc[df_sub['Adsorbate'] == 'HOCO']
        HOCO = HOCOs[HOCOs.Energy == HOCOs.Energy.min()]
        E_HOCO = HOCO.Energy.values[0]
        Eb_HOCO = E_HOCO - E_Surface - E_CO2g - 0.5 * E_H2g
        G_HOCO = E_HOCO + Gcor_HOCO - E_Surface - G_CO2g - 0.5 * G_H2g
        
        COs = df_sub.loc[df_sub['Adsorbate'] == 'CO']
        CO = COs[COs.Energy == COs.Energy.min()]
        E_CO = CO.Energy.values[0]
        Eb_CO = E_CO - E_Surface - E_COg
        G_CO = E_CO + Gcor_CO + G_H2Og - E_Surface - G_H2g - G_CO2g
        
        Hs = df_sub.loc[df_sub['Adsorbate'] == 'H']
        H = Hs[Hs.Energy == Hs.Energy.min()]
        E_H = H.Energy.values[0]
        Eb_H = E_H - E_Surface - 0.5 * E_H2g
        G_H = E_H + Gcor_H - E_Surface - 0.5 * G_H2g
        
        OHs = df_sub.loc[df_sub['Adsorbate'] == 'OH']
        OH = OHs[OHs.Energy == OHs.Energy.min()]
        E_OH = OH.Energy.values[0]
        Eb_OH = E_OH - E_Surface - E_H2Og + 0.5 * E_H2g
        G_OH = E_OH + Gcor_OH - E_Surface - G_H2Og + 0.5 * G_H2g
        
        Binding_energy = [Eb_HOCO, Eb_CO, Eb_H, Eb_OH]
        Free_energy = [G_HOCO, G_CO, G_H, G_OH] # free energy according to reaction equations
        df_stack = pd.concat([HOCO, CO, H, OH], axis=0)
        df_stack['BE'] = Binding_energy
        df_stack['FE'] = Free_energy
        df_new = df_new.append(df_stack, ignore_index=True)
        
        surfaces.append(Surface.Surface.values[0])
        step_ini.append(0)
        step_HOCO.append(G_HOCO)
        step_CO.append(G_CO)
        step_final.append(FE_final)
        
        Eb_HOCOs.append(Eb_HOCO)
        Eb_COs.append(Eb_CO)
        Eb_Hs.append(Eb_H)
        Eb_OHs.append(Eb_OH)
        
    """
    Save the most stable site into excel
    """
    with pd.ExcelWriter(xls_name, engine='openpyxl', mode='a') as writer:
        df_new.to_excel(writer, sheet_name='Ori_Stable', float_format='%.3f')
    
    """
    Save free energy sheet to excel
    """
    tuples = {'Surface': surfaces,
              '* + CO2': step_ini,
              '*HOCO': step_HOCO,
              '*CO': step_CO,
              '* + CO': step_final,
              }
    df_FE = pd.DataFrame(tuples)
    with pd.ExcelWriter(xls_name, engine='openpyxl', mode='a') as writer:
        df_FE.to_excel(writer, sheet_name=sheet_free_energy, index=False, float_format='%.3f')
        
    
    """
    Save binding energy sheet to excel
    """
    tuples = {'Surface': surfaces,
              '*HOCO': Eb_HOCOs,
              '*CO': Eb_COs,
              '*H': Eb_Hs,
              '*OH': Eb_OHs,
              }
    df_BE = pd.DataFrame(tuples)
    with pd.ExcelWriter(xls_name, engine='openpyxl', mode='a') as writer:
        df_BE.to_excel(writer, sheet_name=sheet_binding_energy, index=False, float_format='%.3f')


def plot_free_enegy(xls_name, sheet_free_energy,):
    
    """
    Plot free energy
    """
    stepsNames, observationName, X = read_excel(xls_name, sheet_free_energy, 1, 5, 1, 35) #load excel data
    stepsNames = ['* + CO$_{2}$', 'HOCO*', 'CO*', '* + CO']  #reload step name for CO2RR
    name_fig_FE = '../data/proj2/{}_{}.jpg'.format(system_name, sheet_free_energy)
    CO2RRdiagram = CO2RRFEDplot(stepsNames, observationName, X, name_fig_FE)
    CO2RRdiagram.plot(title=sheet_free_energy)
    plt.legend(loc = "lower left", bbox_to_anchor=(0.00, -0.50, 0.8, 1.02), ncol=5, borderaxespad=0)
    plt.show()


def plot_binding_energy(xls_name, sheet_binding_energy):
    """
    Plot binding energy
    """
    stepsNames, observationName, X = read_excel(xls_name, 'CO2RR_BE', 1, 5, 1, 35) #load excel data
    col1 = [2, 2, 2, 3, 3, 5] #column in excel
    col2 = [3, 5, 4, 5, 4, 4] #column in excel
    
    plt.figure(figsize=(18, 16), dpi = 300)
    name_fig_BE = '../data/proj2/{}_{}.jpg'.format(system_name, sheet_binding_energy)
    M  = 3
    i = 0
    for m1 in range(M-1):
        for m2 in range(M):
            ax = plt.subplot(M, M, m1*M + m2 + 1)
            xcol = col1[i] - 2 
            ycol = col2[i] - 2
            descriper1 = (X[:, xcol]).astype(float) #step2-step1
            descriper2 = (X[:, ycol]).astype(float) #step3-step4
            sr = ScalingRelationPlot(descriper1, descriper2, observationName, name_fig_BE)
            sr.plot(ax = ax, save=False, title='', xlabel=stepsNames[xcol], ylabel=stepsNames[ycol],dotcolor='red', linecolor='red')
            i+=1
    plt.show()
    
if __name__ == '__main__':
    system_name = 'PdHy'
    db_name = '../data/proj2/collect_vasp_PdHy.db' # the only one needed
    xls_name = '../data/proj2/collect_vasp_PdHy.xlsx'
    sheet_free_energy = 'CO2RR_FE'
    sheet_binding_energy = 'CO2RR_BE'
    db = connect(db_name)
    if True:
        db2xls(system_name, xls_name, db, sheet_free_energy, sheet_binding_energy)
    plot_free_enegy(xls_name, sheet_free_energy,)
    plot_binding_energy(xls_name, sheet_binding_energy)
    
