# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:08:11 2021

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

# theta_star = 7/9
theta_COOH = 0.8
theta_CO = 0.2

theta_star = 1 - theta_COOH - theta_CO

def scaling(EHOCO, ECO, T):
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
    # ECO = 0.67 * EHOCO - 1.06 #island
    # EH  = 0.25 * EO + 0.07
    # EOH = 0.45 * EO - 1.22
    
    # reaction energies
    DE1 = EHOCO
    DE2 = ECO - EHOCO - E_CO2g - E_H2g + E_H2Og + E_COg
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
    # k3 = A_prime  * np.exp(- beta * b * DG3)
    k3 = 10**13 * np.exp(- beta * ECO)

    return np.array([k1, k2, k3]), np.array([K1, K2, K3])

def r1_rds(EHOCO, ECO, T, **ps):
    pCO = ps.get('CO', 0.055)
    pCO2 = ps.get('CO2', 1.)
    ks, Ks = scaling(EHOCO, ECO, T)
    r1 = ks[0] * theta_star * pCO2 - ks[0]/Ks[0] * theta_COOH
    return r1

def r2_rds(EHOCO, ECO, T, **ps):
    pCO = ps.get('CO', 0.055)
    pCO2 = ps.get('CO2', 1.)
    ks, Ks = scaling(EHOCO, ECO, T)
    r2 = ks[1] * theta_COOH - ks[1]/Ks[1] * theta_CO
    return r2

def r3_rds(EHOCO, ECO, T, **ps):
    pCO = ps.get('CO', 1)
    pCO2 = ps.get('CO2', 1.)
    ks, Ks = scaling(EHOCO, ECO, T)
    r3 = ks[2] * theta_CO - ks[2]/Ks[2] * theta_star * pCO
    return r3

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
    r1s = np.empty((N,N))
    r2s = np.empty((N,N))
    r3s = np.empty((N,N))
    rmin = np.empty((N,N))
    for i, EHOCO in enumerate(EHOCOs):
        for j, ECO in enumerate(ECOs):
            r1s[i][j] = r1_rds(EHOCO, ECO, T)     # (1) happens once for every H2O formed
            r2s[i][j] = r2_rds(EHOCO, ECO, T) # (2) happens once for every 2 H2O formed
            r3s[i][j] = r3_rds(EHOCO, ECO, T)     # (3) happens once for every H2O formed
            rmin[i][j] = min(r1s[i][j], r2s[i][j], r3s[i][j])
    # print(r1s)
    # data for the elements
    metals = EHOCO_d.keys()
    rN_m = np.empty(len(metals))
    EHOCO_m = np.empty(len(metals))
 
    # plots
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8, 6), dpi = 300)
    ax = fig.add_subplot(111)
    # X, Y = np.meshgrid(EHOCOs, ECOs)
    print(r3s)
    # cp = ax.contourf(X, Y, np.log10(22.2 * (r1_rds(X, Y, T) + r2_rds(X, Y, T) + r3_rds(X, Y, T))))
    cp = ax.contourf(EHOCOs, ECOs,  np.log10(22.2 * r2s))
    # cp = ax.contourf(EHOCOs, ECOs, r1s)
    bar = fig.colorbar(cp) # Add a colorbar to a plot
    ax.set_title('Kinetic volcano for CO evolution')
    ax.set_xlabel('E(HOCO) (eV)')
    ax.set_ylabel('E(CO) (eV)')
    bar.set_label('$log_{10}(j/{\mu}Acm^{-2})$')
    for i,metal in enumerate(metals):
        plt.plot(EHOCO_d[metal], ECO_d[metal], 'o', color='black')  
    plt.show()
    
    # plt.figure(figsize=(8, 6), dpi = 100)
    # plt.semilogy(EHOCOs, r1s, '--k', label='(1) RDS')
    # plt.semilogy(EHOCOs, r2s, '--g', label='(2) RDS')
    # plt.xlabel(r'$\Delta E_{\mathrm{HOCO*}}$ (eV)')
    # plt.ylabel('T.O.F. (s$^{-1}$)')
    # plt.ylim([0.1, np.exp(40)])
    # plt.legend(loc=2)
    # plt.savefig('H2ox_sabatier.png')
    # if 1:  # Plot volcano?
    #     plt.semilogy(EHOCOs, r3s, '--r', label='(3) RDS')
    #     plt.semilogy(EHOCOs, rmin,'-b', label='min(rate)')
    #     print(EHOCO_m, rN_m)
    #     for EHOCO, rN, metal in zip(EHOCO_m, rN_m, metals):
    #         plt.plot(EHOCO, rN, 'ok')
    #         # plt.text(EHOCO, rN, metal)
    #     plt.legend(loc=2)
    #     plt.savefig('H2ox_sabatier_metals.png')
    # plt.show()