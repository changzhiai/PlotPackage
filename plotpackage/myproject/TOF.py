# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 14:06:27 2021

@author: changai
"""

import numpy as np

_kB = 8.617e-5 # Boltzmann constant in eV/K
_h = 4.136e-15  # Planck constant in eV*s
_Sg = 0.002 # eV/K
EH2O = -2.51 # eV

def scaling(EO, T):
    """ Calculate forward rate constants and equilibrium constants 
    as function of the EO descriptor and temperature T.
    """
    beta = 1. / ( _kB * T ) 
    nu_0 = (_kB * T) / _h
    print('nu_0', nu_0)
    # scaling relations
    EH  = 0.25 * EO + 0.07
    EOH = 0.45 * EO - 1.22
    # reaction energies
    DE1 = 2 * EH 
    DE2 = 2 * EO 
    DE3 = EOH - EO - EH
    DE4 = EH2O - EOH - EH
    # Reaction free energies
    DG1 = DE1 + T * _Sg
    DG2 = DE2 + T * _Sg
    DG3 = DE3
    DG4 = DE4 - T * _Sg
    # Equilibrium constants
    K1 = np.exp( - beta * DG1 )
    K2 = np.exp( - beta * DG2 )
    K3 = np.exp( - beta * DG3 )
    K4 = np.exp( - beta * DG4 )
    # activation barriers from scaling
    Ea1 = max(DE1, 0)
    Ea2 = max(0.81 * DE2 + 1.95, DE2, 0)
    Ea3 = max(0.22 * DE3 + 1.11, DE3, 0)
    Ea4 = max(DE4, 0)
    #print(EO, Ea1, Ea2, Ea3, Ea4)
    k1 = nu_0 * np.exp( - _Sg / _kB ) * np.exp(- beta * Ea1) # rate with entropy loss
    k2 = nu_0 * np.exp( - _Sg / _kB ) * np.exp(- beta * Ea2)
    k3 = nu_0 * np.exp(- beta * Ea3)
    k4 = nu_0 * np.exp(- beta * Ea4) 
    return np.array([k1, k2, k3, k4]), np.array([K1, K2, K3, K4])

def r1_rds(EO, T, **ps):
    pO2 = ps.get('O2', 1.)
    pH2 = ps.get('H2', 1.)
    pH2O = ps.get('H2O', 1.)
    ks, Ks = scaling(EO, T)
    lO = np.sqrt( Ks[1] * pO2 )
    lH = np.sqrt( pH2O / ( Ks[2] * Ks[3] * lO ) )
    lOH = pH2O / (Ks[3] * lH)
    r1 = ( ks[0] * pH2 - ks[0]/Ks[0] * lH**2 ) / ( 1 + lH + lOH + lO )**2
    return r1

def r2_rds(EO, T, **ps):
    pO2 = ps.get('O2', 1.)
    pH2 = ps.get('H2', 1.)
    pH2O = ps.get('H2O', 1.)
    ks, Ks = scaling(EO, T)
    lH = np.sqrt(Ks[0] * pH2)
    lOH = pH2O / ( Ks[3] * lH )
    lO = pH2O / (Ks[2] * Ks[3] * lH**2 )
    r2 = ( ks[1] * pO2 - ks[1] / Ks[1] * lO**2 ) / ( 1 + lO + lH + lOH )**2
    return r2

def r3_rds(EO, T, **ps):
    pO2 = ps.get('O2', 1.)
    pH2 = ps.get('H2', 1.)
    pH2O = ps.get('H2O', 1.)
    ks, Ks = scaling(EO, T)
    lH = np.sqrt(Ks[0] * pH2)
    lO = np.sqrt(Ks[1] * pO2)
    lOH = pH2O / ( Ks[3] * lH )
    r3 = ( ks[2] * lO * lH - ks[2] / Ks[2] * lOH ) / ( 1 + lO + lH + lOH )**2
    return r3

EO_d = {'Au':  0.245,
        'Cu': -1.3,
        'Pt': -0.75,
        'Ag': -0.315,
        'Rh': -1.8,
        'Pd': -0.8,
        }

if __name__ == '__main__':
    T = 500.
    N = 100
    EOs = np.linspace(-2.5, 0.5, N)
    # data from scaling
    r1s = np.empty(N)
    r2s = np.empty(N)
    r3s = np.empty(N)
    rmin = np.empty(N)
    for i, EO in enumerate(EOs):
        r1s[i] = r1_rds(EO, T)     # (1) happens once for every H2O formed
        r2s[i] = 2 * r2_rds(EO, T) # (2) happens once for every 2 H2O formed
        r3s[i] = r3_rds(EO, T)     # (3) happens once for every H2O formed
        rmin[i] = min(r1s[i], r2s[i], r3s[i])
    # data for the elements
    metals = EO_d.keys()
    rN_m = np.empty(len(metals))
    EO_m = np.empty(len(metals))
    for i,metal in enumerate(metals):
        EO_m[i] = EO_d[metal]
        rN_m[i] = min(r1_rds(EO_d[metal], T), r2_rds(EO_d[metal], T) )
    # plots
    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.semilogy(EOs, r1s, '--k', label='(1) RDS')
    plt.semilogy(EOs, r2s, '--g', label='(2) RDS')
    plt.xlabel(r'$\Delta E_{\mathrm{O*}}$ (eV)')
    plt.ylabel('T.O.F. (s$^{-1}$)')
    plt.legend(loc=2)
    plt.savefig('H2ox_sabatier.png')
    if 1:  # Plot volcano?
        plt.semilogy(EOs, r3s, '--r', label='(3) RDS')
        plt.semilogy(EOs, rmin,'-b', label='min(rate)')
        for EO, rN, metal in zip(EO_m, rN_m, metals):
            plt.plot(EO, rN, 'ok')
            plt.text(EO, rN, metal)
        plt.legend(loc=2)
        plt.savefig('H2ox_sabatier_metals.png')
    plt.show()