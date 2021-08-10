# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 17:08:11 2021

@author: changai
"""

import numpy as np
from numpy import exp, log
from CO2toCO_acid import CO2toCO
import matplotlib.pyplot as plt

G_CO2g = -18.418 # eV
G_H2g = -7.096# eV
G_H2Og = -12.827 # eV
G_COg = -12.564 # eV

kB = 8.617e-5 # Boltzmann constant in eV/K
hplanck = 4.135669e-15 # eV s
T0 = 297.15
Gact0 = Gact1 = Gact2 = 0.475 # activative free energy
tc0 = tc1 = tc2 = 0.5  #transition state coefficency
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


if __name__ == '__main__':
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
    E_CO_e = np.linspace(-1.5, 1., N)
    E_HOCO_e = np.linspace(-1.2, 1.8, M)
    # EHOCOs = np.linspace(-1, 2, N)
    # ECOs = np.linspace(-2, 0, N)

    jmax = 10.0e3 # exptl current plateau's at 10 mA/cm2 
    jmin = 0.1
    for j, E_CO in enumerate(E_CO_e):
        for i, E_HOCO in enumerate(E_HOCO_e):
            k1, K1, k2, K2, k3, K3 = get_rates(nu_e, nu_c, E_HOCO, E_CO, U, T=T0)
            rm = CO2toCO(pCO2, pCO, xH2O, cHp, k1, K1, k2, K2, k3, K3)
            # rm = CO2toCO(pCO2, pCO, xH2O, cOHm, k1, K1, k2, K2, k3, K3, T0)
            thetas, rates = rm.solve()
            # print(rates)
            rate = min(jmax, rates[0])
            rate = max(jmin, rate)
            R[i,j] = np.log10(rate)
            Thetas[i,j,:] = thetas

    # data for the elements
    metals = ECO_d.keys()

    from matplotlib import rc
    rc('font', **{'family':'sans-serif','sans-serif':['Helvetica'], 'size':8})
    #rc('text', usetex=True)
    
    plt.figure(1, dpi=300)
    plt.clf()
    plt.subplots_adjust(left=.16, bottom=.16, right=.96, top=.90)
    # pl.hold(1)
    contours = np.linspace(np.log10(jmin), np.log10(jmax), 11) 
    plt.contourf(E_CO_e, E_HOCO_e, R, contours, cmap=plt.cm.jet)
    # E_HOCO_scaling = HOCO_CO_scaling(E_CO_e)
    # pl.plot(E_CO_e, E_HOCO_scaling,'-k', lw=1)
    # for i in range(len(ECO_d)): # elements
    #     pl.text(ECO_d[i], EHOCO_d[i], texts[i], 
    #             ha='center', va='center')
    for i,metal in enumerate(metals):
        plt.plot(ECO_d[metal], EHOCO_d[metal], 'o', color='black') 
        plt.text(ECO_d[metal], EHOCO_d[metal]+0.05, metal, fontsize=12, horizontalalignment='center', verticalalignment='bottom')
    
    #linear fiting and plot linear line
    m, b = np.polyfit(list(ECO_d.values()), list(EHOCO_d.values()), 1)
    # pl.plot(list(ECO_d.values()), m * np.array(list(ECO_d.values())) + b, linewidth=1, color='black')
    plt.axline((list(ECO_d.values())[0], list(ECO_d.values())[0]*m +b), slope=m, color='black')
    plt.xlim([E_CO_e[0]+0.1, E_CO_e[-1]-0.1])
    plt.ylim([E_HOCO_e[0]+0.1, E_HOCO_e[-1]-0.1])
    plt.colorbar(ticks=np.arange(min(contours), max(contours), 0.5))
    plt.title(r'log$_{10}$(j/$\mu$Acm$^{-2}$)')
    plt.xlabel(r'$E_{\mathrm{CO}}$ (eV)')
    plt.ylabel(r'$E_{\mathrm{HOCO}}$ (eV)')
    plt.savefig('../data/CO2toCO_rate_vs_HOCO_CO.png', dpi=300)
    plt.show()
    
    if 1: # test K1, K2, K3 using Cu(211) as an example
        N = 10
        dG1 = []
        dG2 = []
        dG3 = []
        U = np.linspace(-1.25, 1, N)
        for i, u in enumerate(U):
            print(i)
            E_HOCO = 0.42967678
            E_CO = -0.36259556 # CO ads energy
            #E_CO = - 0.3 # CO ads energy
            # U = -0.0
            K1 = get_K1(E_HOCO, U, T=T0)
            K2 = get_K2(E_HOCO, E_CO, U, T=T0)
            K3 = get_K3(E_CO, U, T=T0)
            # K1_s = get_K1(E_CO, U, T=T0)
            # K2_s = get_K2(E_CO, U, T=T0)
            # K3_s = get_K3(E_CO, U, T=T0)
            dG1.append(-kB*T0*np.log(K1))
            dG2.append(-kB*T0*np.log(K2))
            dG3.append(-kB*T0*np.log(K3))
            # dG1_s, dG2_s, dG3_s = -kB*T0*np.log(K1_s), -kB*T0*np.log(K2_s), -kB*T0*np.log(K3_s)
            # print(ddG_HOCO, ddG_CO)
            # print(dG1, dG1 + dG2, dG1 + dG2 + dG3)
            # print(dG1_s, dG1_s + dG2_s, dG1_s + dG2_s + dG3_s)
        plt.figure(1, dpi=300)
        plt.plot(U, dG1, color='black')
        plt.plot(U, dG2, color='red')
        plt.plot(U, dG3, color='blue')
        plt.xlabel(r'Potential (V)')
        plt.ylabel(r'${\Delta}$G (eV)')

    # plots
    # import matplotlib.pyplot as plt
    # fig = plt.figure(figsize=(8, 6), dpi = 300)
    # ax = fig.add_subplot(111)
    # # X, Y = np.meshgrid(EHOCOs, ECOs)
    # print(r3s)
    # # cp = ax.contourf(X, Y, np.log10(22.2 * (r1_rds(X, Y, T) + r2_rds(X, Y, T) + r3_rds(X, Y, T))))
    # cp = ax.contourf(EHOCOs, ECOs,  np.log10(22.2 * r2s))
    # # cp = ax.contourf(EHOCOs, ECOs, r1s)
    # bar = fig.colorbar(cp) # Add a colorbar to a plot
    # ax.set_title('Kinetic volcano for CO evolution')
    # ax.set_xlabel('E(HOCO) (eV)')
    # ax.set_ylabel('E(CO) (eV)')
    # bar.set_label('$log_{10}(j/{\mu}Acm^{-2})$')
    # for i,metal in enumerate(metals):
    #     plt.plot(EHOCO_d[metal], ECO_d[metal], 'o', color='black')  
    # plt.show()
