# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 17:38:39 2021

@author: changai
"""

import numpy as np
# import scipy.constants
# _e = scipy.constants.physical_constants['electron mass'][0]
_kB = 8.617e-5 # Boltzmann constant in eV/K
_h = 4.136e-15  # Planck constant in eV*s
_Sg = 0.002 # eV/K
# EH2O = -2.51 # eV

E_CO2g = -18.459 # eV
E_H2g = -7.158 # eV
E_H2Og = -12.833 # eV
E_COg = -12.118 # eV
limiting_potenital = 0


def scaling(EHOCO, ECO, T):
    """ Calculate forward rate constants and equilibrium constants 
    as function of the EO descriptor and temperature T.
    """
    
    # reaction energies
    DE1 = EHOCO
    DE2 = ECO - EHOCO - E_CO2g - E_H2g + E_H2Og + E_COg
    DE3 = -ECO
    # limiting_potenital = max(DE1, DE2, DE3)
    limiting_potenital = max(DE1/(-1), DE2/(-1), DE3/(-1)) 

    return limiting_potenital


EHOCO_d = {
    "Pd": 0.42967678,
    # "Sc": -0.08249209,
    "Ti": 0.09677125,
    "V": 0.08057561,
    "Mn": -0.28851255,
    "Fe": -0.15955723,
    "Co": 0.47024493,
    "Ni": 0.67499474,
    "Cu": 1.22119557,
    # "Zn": 0.54101516,
    # "Y": -2.76843569,
    # "Zr": -1.44950915,
    "Nb": 0.14885378,
    "Mo": 0.12097152,
    "Ru": 0.32770351,
    "Rh": 0.53514527,
    "Ag": 1.57118722
}

ECO_d = {
    "Pd": -0.36259556,
    # "Sc": -0.53887365,
    "Ti": -0.7954072,
    "V": -1.07970746,
    "Mn": -1.31038448,
    "Fe": -1.3575169,
    "Co": -0.90030351,
    "Ni": -0.49399452,
    "Cu": -0.25260203,
    # "Zn": -0.11389156,
    # "Y": -2.81622299,
    # "Zr": -0.10195565,
    "Nb": -0.94465297,
    "Mo": -0.76108613,
    "Ru": -1.20819791,
    "Rh": -0.6742065,
    "Ag": -0.09120301
}

if __name__ == '__main__':
    T = 297.15
    N = 100
    EHOCOs = np.linspace(-1, 2, N)
    ECOs = np.linspace(-2, 0, N)
    # data from scaling
    limit = np.empty((N,N))

    for i, EHOCO in enumerate(EHOCOs):
        for j, ECO in enumerate(ECOs):
            limit[i][j] = scaling(EHOCO, ECO, T) 

    # data for the elements
    metals = EHOCO_d.keys()
    rN_m = np.empty(len(metals))
    EHOCO_m = np.empty(len(metals))
   
    # plots
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8, 6), dpi = 300)
    ax = fig.add_subplot(111)

    cp = ax.contourf(EHOCOs, ECOs,  limit)
    # cp = ax.contourf(EHOCOs, ECOs, r1s)
    bar = fig.colorbar(cp) # Add a colorbar to a plot
    ax.set_title('Limiting potential')
    ax.set_xlabel('E(HOCO) (eV)')
    ax.set_ylabel('E(CO) (eV)')
    bar.set_label('Limiting potential (V)')
    for i,metal in enumerate(metals):
        plt.plot(EHOCO_d[metal], ECO_d[metal], 'o', color='black')
        plt.annotate(metal, (EHOCO_d[metal], ECO_d[metal]+0.005), fontsize=12, horizontalalignment='center', verticalalignment='bottom')
    plt.show()
