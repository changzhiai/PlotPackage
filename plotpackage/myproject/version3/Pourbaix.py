# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 16:56:18 2022

@author: changai
"""

"""
Elementary steps:
    
CO2(g) + * + H+ + e- -> HOCO*   (dG1)
dG1 = G_HOCO* - G_CO2g - G* - 1/2 G_H2g
Gb_HOCO = dG1

HOCO* + H+ + e- -> CO* + H2O(g) (dG2)
dG2 = G_CO* + G_H2Og - G_HOCO* - 1/2 G_H2g
Gb_CO_ref_e = dG2 - dG1 # reference electrochemical initial step

CO* -> CO(g) + *                  (dG3)
dG3 = G_COg + G* - G_CO*
Gb_CO = -dG3

H+ + e- + * -> H*                 (dG4)
dG4 = G_H - G* - 1/2 G_H2g
Gb_H = dG4

H2O(g) + * -> OH* + H+ + e-       (dG5)
dG5 = G_OH + 1/2 G_H2g - G* - G_H2O(g)
Gb_OH = dG5

Pd55Nb9H64 -> Pd64H64 - 9*Pd2+ + 9*Nb3+ + 9*e-         (dG6)
dG6 = G_Pd64H64 - 9*G_Pd2+ + 9*G_Nb3+ - 9*eU - G_Pd55Nb9H64

# Pd63NbH64 -> Pd64H64 - Pd2+ + Nb3+ + e-         (dG6)
# dG6 = G_Pd64H64 - G_Pd2+ + G_Nb3+ - eU - G_Pd63NbH64


G = E_dft + E_zpe + C_p - TS

delta_G(U, pH) = delta_G(U=0, pH=0) - ne * U + n * k_B * T * pH * ln(10)
Here e is -1, reference Andrew`s paper
μ( H+(aq)) + μ(e-) = 1/2μH2(g) - eUSHE + kBT ln(10) pH from Heine`s theis

Note:   alpha = np.log(10) * self.kT
        if name == 'e-':
            energy = -U
        elif name == 'H+(aq)':
            energy = -pH * alpha
        , which is from ase
    
"""

from pcat.lib.io import pd_read_excel
import numpy as np
import pcat.utils.constants as const
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams.update({'mathtext.default':  'regular', 'figure.dpi': 150})

def pourbaix_diagram(U, pH):
    """Get pourbaix diagram as a function of applied potential and pH value"""
    # df = pd_read_excel(filename=xls_name, sheet=sheet_name_dGs)
    # df = df.iloc[10]
    # surface = df['Surface']
    # dG1 = df['dG1']
    # dG2 = df['dG2']
    # dG3 = df['dG3']
    # dG4 = df['dG4']
    # dG5 = df['dG5']
    
    # for Nb in configuration of overlayer
    E_Pd64H64 = -285.3708828
    E_Pd55Nb9H64 = -336.2919741
    E_Pd_bulk = -1.950920655
    E_Nb_bulk = -7.244883085
    G_Pd2plus = E_Pd_bulk + 2 * 0.915 + 0.0592 * np.log(10**(-6))
    G_Nb3plus = E_Nb_bulk + 3 * 0.915 + 0.0592 * np.log(10**(-6))
    dG1 = 0.624
    dG2 = -0.725
    dG3 = -0.224
    dG4 = 0.467
    dG5 = -0.132
    
    # for pure PdH
    # dG1 = 0.820
    # dG2 = -0.603
    # dG3 = 0.093
    # dG4 = 0.501
    # dG5 = 1.581
    
    
    # N, M = 20*4, 20*4
    # N, M = 20, 20
    # U_model = np.linspace(min(U), max(U), N)
    # pH_model = np.linspace(min(pH), max(pH), M)
    # pH_model = [0]
    
    kB = const.kB
    T = 297.15
    
    N, M = 200, 200
    
    # pH = 0
    U_model = np.linspace(min(U), max(U), N)
    if type(pH) == int or type(pH) == float:
        pH_model = [pH]
    else:
        pH_model = np.linspace(min(pH), max(pH), M)
    Us = []
    pHs = []
    Gb_HOCOs = []
    Gb_CO_ref_es = []
    Gb_COs = []
    Gb_Hs = []
    Gb_OHs = []
    G_dissolve_Nb_overlys = []
    colors = []
    Us_acc = np.zeros(5) # accumulate U in order to calculate average U
    pHs_acc = np.zeros(5)
    count = np.zeros(5)
    for i, ph in enumerate(pH_model):
        for j, u in enumerate(U_model):
            Gb_HOCO = dG1 + u + kB * T * ph * np.log(10)
            Gb_CO_ref_e = dG2 - dG1
            # Gb_CO = dG2 - dG1
            Gb_CO = -dG3
            Gb_H = dG4 + u + kB * T * ph * np.log(10)
            Gb_OH = dG5 - u - kB * T * ph * np.log(10)
            
            # G_dissolve_Pd_overly = (E_Pd64H64 - 9*G_Pd2plus + 9*G_Nb3plus - 9*u - E_Pd55Nb9H64) / 9.0
            G_dissolve_Nb_overly = (E_Pd64H64 - 9*G_Pd2plus + 9*G_Nb3plus - 9*u - E_Pd55Nb9H64) / 9.0
            # print(u, Gb_HOCO)
            # plt.scatter(u, Gb_HOCO)
            Us.append(u)
            pHs.append(ph)
            
            # Gb_HOCO = Gb_HOCO/4
            # Gb_CO = Gb_CO/2
            # Gb_H = Gb_H
            # Gb_OH = Gb_OH/2
            
            Gb_HOCOs.append(Gb_HOCO)
            Gb_CO_ref_es.append(Gb_CO_ref_e)
            Gb_COs.append(Gb_CO)
            Gb_Hs.append(Gb_H)
            Gb_OHs.append(Gb_OH)
            
            G_dissolve_Nb_overlys.append(G_dissolve_Nb_overly)
            
            min_dot = min(Gb_HOCO, Gb_CO, Gb_H, Gb_OH, G_dissolve_Nb_overly)
            if min_dot == Gb_HOCO:
                color = 'blue'
                Us_acc[0] += u
                pHs_acc[0] += ph
                count[0] += 1
            elif  min_dot == Gb_CO:
                color = 'orange'
                Us_acc[1] += u
                pHs_acc[1] += ph
                count[1] += 1
            elif  min_dot == Gb_H:
                color = 'green'
                Us_acc[2] += u
                pHs_acc[2] += ph
                count[2] += 1
            elif  min_dot == Gb_OH:
                color = 'brown'
                Us_acc[3] += u
                pHs_acc[3] += ph
                count[3] += 1
            elif min_dot == G_dissolve_Nb_overly:
                color = 'red'
                Us_acc[4] += u
                pHs_acc[4] += ph
                count[4] += 1
            colors.append(color)
            
    if type(pH) == int or type(pH) == float:
        plt.plot(Us, Gb_HOCOs, label='Gb_HOCOs')
        # plt.plot(Us, Gb_CO_ref_es, label='Gb_CO_ref_es')
        plt.plot(Us, Gb_COs, label='Gb_COs')
        plt.plot(Us, Gb_Hs, label='Gb_Hs')
        plt.plot(Us, Gb_OHs, label='Gb_OHs')
        plt.plot(Us, G_dissolve_Nb_overlys, label='G_dissolve_Nb_overly')
        plt.xlabel('$U_{SHE}$')
        plt.ylabel('$\Delta G$ (eV/per adsorbate)')
        plt.legend()
        plt.show()
    else:
        plt.scatter(pHs, Us, c=colors, marker='o', zorder=2)
        plt.xlabel('pH')
        plt.ylabel('$U_{SHE}$ (V)')
        for i, txt in enumerate(['Gb_HOCOs', 'Gb_COs', 'Gb_Hs', 'Gb_OHs', 'G_dissolve_Nb_overly']):
            x = pHs_acc[i]/count[i]
            y = Us_acc[i]/count[i] 
            plt.text(x, y, txt, horizontalalignment='center')
        
    tuples = {'Us': Us,
              'pHs': pHs,
              'Gb_HOCOs': Gb_HOCOs,
              'Gb_CO_ref_es': Gb_CO_ref_es,
              'Gb_COs': Gb_COs,
              'Gb_Hs': Gb_Hs,
              'Gb_OHs': Gb_OHs,
              'Colors': colors,
              }
    df_FE = pd.DataFrame(tuples)
    
        
if __name__ == '__main__':
    
    system_name = 'collect_vasp_PdHy_v3'
    
    xls_name = f'../data/{system_name}.xlsx'
    fig_dir = '../figures'
    
    sheet_name_dGs = 'dGs'
    
    U = [-2, 3]
    pH = 0
    pourbaix_diagram(U, pH)
    
    pH = [0, 14]
    pourbaix_diagram(U, pH)
    
    