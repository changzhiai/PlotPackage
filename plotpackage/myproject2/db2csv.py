# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 13:55:28 2022

@author: changai
"""

from ase.db import connect
import pandas as pd

db_name = '../data/proj2/collect_vasp_PdHy.db'
xls_name = '../data/proj2/collect_vasp_PdHy.xlsx'
db = connect(db_name)


# uniqueids = []
# energies = []
# for row in db.select():
#     uniqueids.append(row.uniqueid)
#     energies.append(row.energy)
    
# tuples = {'unique_id': uniqueids,
#           'energy': energies,
#          }
# df = pd.DataFrame(tuples)
# df.to_excel('../data/proj2/collect_vasp_PdHy.xlsx',,sheet_name='origin_db')

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
df.to_excel(xls_name, sheet_name='dft_e')

E_H2 = -7.158 # eV
E_CO2 = -18.459
E_H2O = -12.833
E_CO = -12.118

df_new  = pd.DataFrame()
uniqueids = df['Id'].astype(int).unique()
for id in uniqueids:
    # print(id)
    df_sub = df.loc[df['Id'].astype(int) == id]
    Surface = df_sub.loc[df_sub['Adsorbate'] == 'surface']
    # print(df_sub)
    HOCOs = df_sub.loc[df_sub['Adsorbate'] == 'HOCO']
    HOCO = HOCOs[HOCOs.Energy == HOCOs.Energy.min()]
    Eb_HOCO = HOCO.Energy.values[0] - Surface.Energy.values[0] - E_CO2 - 0.5 * E_H2
    
    COs = df_sub.loc[df_sub['Adsorbate'] == 'CO']
    CO = COs[COs.Energy == COs.Energy.min()]
    Eb_CO = CO.Energy.values[0] - Surface.Energy.values[0] -E_CO
    
    Hs = df_sub.loc[df_sub['Adsorbate'] == 'H']
    H = Hs[Hs.Energy == Hs.Energy.min()]
    Eb_H = H.Energy.values[0] - Surface.Energy.values[0] - 0.5 * E_H2
    
    OHs = df_sub.loc[df_sub['Adsorbate'] == 'OH']
    OH = OHs[OHs.Energy == OHs.Energy.min()]
    Eb_OH = OH.Energy.values[0] - Surface.Energy.values[0] - E_H2O + 0.5 * E_H2
    
    Binding_energy = [Eb_HOCO, Eb_CO, Eb_H, Eb_OH]
    df_stack = pd.concat([HOCO, CO, H, OH], axis=0)
    df_stack['Binding_energy'] = Binding_energy
    df_new = df_new.append(df_stack, ignore_index=True)

# df_new.to_excel(xls_name, sheet_name='dft_min_e')
with pd.ExcelWriter(xls_name, engine='openpyxl', mode='a') as writer:
    df_new.to_excel(writer, sheet_name='dft_min_e')
    
    
    
