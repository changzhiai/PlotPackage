# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 14:55:55 2021

@author: changai
"""

import numpy as np

_kB = 8.617e-5 # Boltzmann constant in eV/K
_h = 4.136e-15  # Planck constant in eV*s
_Sg = 0.002 # eV/K
# EH2O = -2.51 # eV

E_CO2g = -18.459 # eV
E_H2g = -7.158 # eV
E_H2Og = -12.833 # eV
E_COg = -12.118 # eV



def scaling(EHOCO, T):
    """ Calculate forward rate constants and equilibrium constants 
    as function of the EO descriptor and temperature T.
    """
    beta = 1. / ( _kB * T ) 
    # nu_0 = (_kB * T) / _h
    # Ea1 = 0
    # Ea2 = 0
    # Ea3 = 0
    A_prime = 3.6 * 10**4
    b = 0.5
    
    # scaling relations
    ECO = 0.67 * EHOCO - 1.06 #island
    # EH  = 0.25 * EO + 0.07
    # EOH = 0.45 * EO - 1.22
    
    # reaction energies
    DE1 = EHOCO
    DE2 = ECO - EHOCO - E_CO2g - E_H2g - E_H2Og + E_COg
    DE3 = -ECO

    # Reaction free energies
    DG1 = DE1 + T * _Sg
    DG2 = DE2 - T * _Sg
    DG3 = DE3 + T * _Sg

    # Equilibrium constants
    K1 = np.exp( - beta * DG1 )
    K2 = np.exp( - beta * DG2 )
    K3 = np.exp( - beta * DG3 )

    # activation barriers from scaling
    # Ea1 = max(DE1, 0)
    # Ea2 = max(0.81 * DE2 + 1.95, DE2, 0)
    # Ea3 = max(0.22 * DE3 + 1.11, DE3, 0)
    # Ea4 = max(DE4, 0)
    #print(EO, Ea1, Ea2, Ea3, Ea4)
    # k1 = nu_0 * np.exp( - _Sg / _kB ) * np.exp(- beta * Ea1) # rate with entropy loss
    # k2 = nu_0 * np.exp( - _Sg / _kB ) * np.exp(- beta * Ea2)
    k1 = A_prime  * np.exp(- beta * b * DG1) # rate with entropy loss
    k2 = A_prime  * np.exp(- beta * b * DG2)
    k3 = 10**13 * np.exp(- beta * ECO)

    return np.array([k1, k2, k3]), np.array([K1, K2, K3])

def r1_rds(EHOCO, T, **ps):
    pCO = ps.get('CO', 0.055)
    pCO2 = ps.get('CO2', 1.)
    ks, Ks = scaling(EHOCO, T)
    r1 = ks[0] * 7/9 * pCO2 - ks[0]/Ks[0] * 1/9
    return r1

def r2_rds(EHOCO, T, **ps):
    pCO = ps.get('CO', 0.055)
    pCO2 = ps.get('CO2', 1.)
    ks, Ks = scaling(EHOCO, T)
    r2 = ks[1] * 1/9 - ks[1]/Ks[1] * 1/9
    return r2

def r3_rds(EO, T, **ps):
    pCO = ps.get('CO', 0.055)
    pCO2 = ps.get('CO2', 1.)
    ks, Ks = scaling(EHOCO, T)
    r3 = ks[2] * 1/9 - ks[2]/Ks[2] * 7/9 * pCO
    return r3

EHOCO_d = {
    'Pd': 0.84367678,
    'Ti': 0.52069347,
    'V': 0.49457561,
    'Mn': 0.12548745,
    'Fe': 0.25444277,
    'Co': 0.88424493,
    'Ni': 1.08899474,
    'Cu': 1.63519557,
    'Nb': 0.56285378,
    'Mo': 0.53497152,
    'Ru': 0.74170351,
    'Rh': 0.94914527,
    'Ag': 1.98430517
}

if __name__ == '__main__':
    T = 500
    N = 100
    EHOCOs = np.linspace(-2.5, 0.5, N)
    # data from scaling
    r1s = np.empty(N)
    r2s = np.empty(N)
    r3s = np.empty(N)
    rmin = np.empty(N)
    for i, EHOCO in enumerate(EHOCOs):
        r1s[i] = r1_rds(EHOCO, T)     # (1) happens once for every H2O formed
        r2s[i] = r2_rds(EHOCO, T) # (2) happens once for every 2 H2O formed
        r3s[i] = r3_rds(EHOCO, T)     # (3) happens once for every H2O formed
        rmin[i] = min(r1s[i], r2s[i], r3s[i])
    # data for the elements
    metals = EHOCO_d.keys()
    rN_m = np.empty(len(metals))
    EHOCO_m = np.empty(len(metals))
    for i,metal in enumerate(metals):
        EHOCO_m[i] = EHOCO_d[metal]
        rN_m[i] = min(r1_rds(EHOCO_d[metal], T), r2_rds(EHOCO_d[metal], T) )
    # plots
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 6), dpi = 100)
    # plt.semilogy(EHOCOs, r1s, '--k', label='(1) RDS')
    plt.semilogy(EHOCOs, r2s, '--g', label='(2) RDS')
    plt.xlabel(r'$\Delta E_{\mathrm{HOCO*}}$ (eV)')
    plt.ylabel('T.O.F. (s$^{-1}$)')
    plt.legend(loc=2)
    plt.savefig('H2ox_sabatier.png')
    if 0:  # Plot volcano?
        plt.semilogy(EHOCOs, r3s, '--r', label='(3) RDS')
        plt.semilogy(EHOCOs, rmin,'-b', label='min(rate)')
        for EHOCO, rN, metal in zip(EHOCO_m, rN_m, metals):
            plt.plot(EHOCO, rN, 'ok')
            plt.text(EHOCO, rN, metal)
        plt.legend(loc=2)
        plt.savefig('H2ox_sabatier_metals.png')
    plt.show()