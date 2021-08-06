# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 12:55:23 2021

@author: changai
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rc("font", family="Verdana",weight='normal')
plt.rcParams.update({'mathtext.default':  'regular' })


# kB   = 8.617e-5 # Boltzmann constant in eV/K
# h    = 4.136e-15  # Planck constant in eV*s
# 
# KT   = kB * T

# pre_pH = kB*T*np.log(10)
# G_H2O  = -12.869    #eV/molecule (Free energy + BEEF correction)
# G_H2   = -7.128     #eV/molecule (Free energy + BEEF correction)
# a_O2   = 2.34*10E-5
# a_H2O  = 1
# A      = 1.23*10E+9  #s-1
# Ea     = 0.26    #eV --> energy barrier fore proton transfer
# pH     = 0


_kB = 8.617e-5 # Boltzmann constant in eV/K
_h = 4.136e-15  # Planck constant in eV*s
_Sg = 0.002 # eV/K
A_prime = 3.6 * 10**4
T = 298.15
b = 0.5
beta = 1. / ( _kB * T )
pH     = 0
pre_pH = _kB*T*np.log(10)
Ea     = 0.26    #eV --> energy barrier fore proton transfer
KT   = _kB * T
A      = 1.23*10E+9  #s-1

E_CO2g = -18.459 # eV
E_H2g = -7.158 # eV
E_H2Og = -12.833 # eV
E_COg = -12.118 # eV
# limiting_potenital = 0
pCO = 0.055
pCO2 = 1.
xH2O  = 1
# Ea     = 0.26    #eV --> energy barrier fore proton transfer

EHOCO = 0.42 # binding energy of HOCO*
ECO = -0.36 # binding energy of CO*

DE1 = EHOCO
DE2 = ECO - EHOCO - E_CO2g - E_H2g + E_H2Og + E_COg
DE3 = -ECO
print(DE1, DE2, DE3)

c_x = []
c_hoco = []
c_co = []
U = np.linspace(-1.25, 1, 29)
for u in U:
    print('potential %.2f'%u)

    # Reaction free energies
    DG1 = DE1 + T * _Sg + u + pre_pH*pH
    DG2 = DE2 - T * _Sg + u + pre_pH*pH
    DG3 = DE3 + T * _Sg + u + pre_pH*pH
    
    # Equilibrium constants
    K1 = np.exp( - beta * DG1 )
    K2 = np.exp( - beta * DG2 )
    K3 = np.exp( - beta * DG3 )
    
    k1 = A_prime  * np.exp(- beta * b * DG1) # rate with entropy loss
    k2 = A_prime  * np.exp(- beta * b * DG2)
    k3 = 10**13 * np.exp(- beta * ECO)
    # k3 = A_prime  * np.exp(- beta * b * DG3)
    
    k1r = k1/K1
    k2r = k2/K2
    k3r = k3/K3
    
    f1 = k1/(k1+k1r)
    f2 = k2/(k2+k2r)
    f3 = k3/(k3+k3r)
    r1 = k1r/(k1+k1r)
    r2 = k2r/(k2+k2r)
    r3 = k3r/(k3+k3r)
    
    def f(t,y):
        X    = y[0]
        HOCO = y[1]
        CO   = y[2]

        dX_dt   = f3*CO - r3*X*pCO - f1*X*pCO2 + r1*HOCO
        dHOCO_dt   = f1*X*pCO2 - r1*HOCO - f2*HOCO + r2*CO*xH2O
        dCO_dt  = f2*HOCO - r2*CO*xH2O - f3*CO + r3*X*pCO
        return np.array([dX_dt, dHOCO_dt, dCO_dt]) 
    
    # def f(t,y):
    #     X    = y[0]
    #     HOCO = y[1]
    #     CO   = y[2]

    #     dX_dt   = k3*CO - k3r*X*pCO - k1*X*pCO2 + k1r*HOCO
    #     dHOCO_dt   = k1*X*pCO2 - k1r*HOCO - k2*HOCO + k2r*CO*xH2O
    #     dCO_dt  = k2*HOCO - k2r*CO*xH2O - k3*CO + k3r*X*pCO
    #     return np.array([dX_dt, dHOCO_dt, dCO_dt]) 
    # print(k1, k2, k3,  k1r, k2r, k3r)
    
    # print('potential %.2f'%u)
    # dG1  = DE1 + T * _Sg + u + pre_pH*pH
    # #print(G1, dG1)
    # F1  = A*np.exp(-Ea/KT)*np.exp(-0.5*dG1/KT)
    # R1  = F1/np.exp(-dG1/KT) 


    # dG2  = DE2 - T * _Sg + u + pre_pH*pH
    # #print(G2, dG2)
    # F2  = A*np.exp(-Ea/KT)*np.exp(-0.5*dG2/KT)
    # R2  = F2/np.exp(-dG2/KT)


    # dG3  = DE3 + T * _Sg + u + pre_pH*pH
    # #print(G3, dG3)
    # F3  = A*np.exp(-Ea/KT)*np.exp(-0.5*dG3/KT)
    # R3  = F3/np.exp(-dG3/KT)


    # f1 = F1/(F1+R1)
    # f2 = F2/(F2+R2)
    # f3 = F3/(F3+R3)
    # r1 = R1/(F1+R1)
    # r2 = R2/(F2+R2)
    # r3 = R3/(F3+R3)
    
    # def f(t,y):
    #     X    = y[0]
    #     HOCO = y[1]
    #     CO   = y[2]

    #     dX_dt   = f3*CO - r3*X*pCO - f1*X*pCO2 + r1*HOCO
    #     dHOCO_dt   = f1*X*pCO2 - r1*HOCO - f2*HOCO + r2*CO*xH2O
    #     dCO_dt  = f2*HOCO - r2*CO*xH2O - f3*CO + r3*X*pCO
    #     return np.array([dX_dt, dHOCO_dt, dCO_dt]) 
    
    t_span = np.array([0,1000])  
    time = np.linspace(t_span[0], t_span[1], 100)
    y0 = np.array([1.0, 0.0, 0.0])
    soln = solve_ivp(f, t_span, y0, t_eval=time)
    t = soln.t
    X = soln.y[0]
    HOCO = soln.y[1]
    CO = soln.y[2]
    
    plt.figure()
    plt.plot(t, X, label='X')
    plt.plot(t, HOCO, label='HOCO')
    plt.plot(t, CO, label='CO')
    plt.legend()
    plt.show()
    print('X=%.2f'%X[-1])
    print('HOCO=%.2f'%HOCO[-1])
    print('CO=%.2f'%CO[-1])
    print(t)
    c_x.append(X[-1])
    c_hoco.append(HOCO[-1])
    c_co.append(CO[-1])

fig,ax=plt.subplots(1,1)
ax.set_xlabel('$U_{RHE}$')
ax.set_ylabel('Coverage (a.u.)')
# plt.xlim(-2, 0)
plt.ylim(0, 1)
plt.plot(U, c_x, label='*',linewidth=1.0,linestyle='solid')
#plt.scatter(U, c_x,linewidth=0.2)
plt.plot(U, c_hoco, label='*HOCO',linewidth=1.0,linestyle='solid')
#plt.scatter(U, c_oh,linewidth=0.2)
plt.plot(U, c_co, label='*CO',linewidth=1.0,linestyle='solid')
#plt.scatter(U, c_o,linewidth=0.2)
plt.legend()
plt.show()
    
# # ###FeN4C10
# # G_MN4 = -489.586
# # G_MN4_O = -494.316
# # G_MN4_OH = -498.488
# # G_MN4_OOH = -501.318
# # ###FeN4C10E
# # #G_MN4 = -328.156
# # #G_MN4_O = -332.836
# # #G_MN4_OH = -337.176
# # #G_MN4_OOH = -339.877
# # ###FeN4C10A
# # #G_MN4 = -308.533
# # #G_MN4_O = -313.175
# # #G_MN4_OH = -317.377
# # #G_MN4_OOH = -320.245 

# # G_Oad = G_H2 + G_MN4_O - G_MN4 - G_H2O
# # G_OHad = 0.5*G_H2 + G_MN4_OH - G_MN4 - G_H2O
# # G_OOHad = 1.5*G_H2 + G_MN4_OOH - G_MN4 - 2*G_H2O

# # G1 = G_OOHad - 4.92
# # G2 = G_Oad - G_OOHad
# # G3 = G_OHad - G_Oad
# # G4 = -G_OHad
# #print(G1,G2,G3,G4)

# U = np.linspace(0.0, 1.2, 29)
# # c_x = []
# # c_o = []
# # c_oh = []
# # c_ooh = []
# for u in U:
# #u = 0.4
# #if u==0.4:
#     print('potential %.2f'%u)
#     dG1  = G1 + u + pre_pH*pH
#     #print(G1, dG1)
#     F1  = A*np.exp(-Ea/KT)*np.exp(-0.5*dG1/KT)
#     R1  = F1/np.exp(-dG1/KT)
    

#     dG2  = G2 + u + pre_pH*pH
#     #print(G2, dG2)
#     F2  = A*np.exp(-Ea/KT)*np.exp(-0.5*dG2/KT)
#     R2  = F2/np.exp(-dG2/KT)
   
#     dG3  = G3 + u + pre_pH*pH
#     #print(G3, dG3)
#     F3  = A*np.exp(-Ea/KT)*np.exp(-0.5*dG3/KT)
#     R3  = F3/np.exp(-dG3/KT)
    
#     dG4  = G4 + u + pre_pH*pH
#     #print(G4, dG4)
#     F4  = A*np.exp(-Ea/KT)*np.exp(-0.5*dG4/KT)
#     R4  = F4/np.exp(-dG4/KT)
    
#     f1 = F1/(F1+R1)
#     f2 = F2/(F2+R2)
#     f3 = F3/(F3+R3)
#     f4 = F4/(F4+R4)
#     r1 = R1/(F1+R1)
#     r2 = R2/(F2+R2)
#     r3 = R3/(F3+R3)
#     r4 = R4/(F4+R4)
#     #print(F1,F2,F3,F4)
#     #print(R1,R2,R3,R4)
#     #print(f1,f2,f3,f4)
#     #print(r1,r2,r3,r4)
#     def f(t,y):
#         X    = y[0]
#         HOCO    = y[1]
#         CO   = y[2]

#         dX_dt   = f4*OH - r4*X*a_H2O - f1*X*a_O2 + r1*OOH
#         dO_dt   = f2*OOH - r2*O*a_H2O - f3*O + r3*OH
#         dOH_dt  = f3*O - r3*OH - f4*OH + r4*X*a_H2O
#         dOOH_dt = f1*X*a_O2 - r1*OOH - f2*OOH + r2*O*a_H2O
#         return np.array([dX_dt, dO_dt, dOH_dt, dOOH_dt]) 
    
#     t_span = np.array([0,1000])  
#     time = np.linspace(t_span[0], t_span[1], 100)
#     y0 = np.array([1.0,0.0,0.0,0.0])
#     soln = solve_ivp(f, t_span, y0, t_eval=time)
#     t = soln.t
#     X = soln.y[0]
#     O = soln.y[1]
#     OH = soln.y[2]
#     OOH = soln.y[3]
    
#     plt.figure()
#     plt.plot(t, X, label='X')
#     plt.plot(t, O, label='O')
#     plt.plot(t, OH, label='OH')
#     plt.plot(t, OOH, label='OOH')
#     plt.legend()
#     plt.show()
#     print('X=%.2f'%X[-1])
#     print('O=%.2f'%O[-1])
#     print('OH=%.2f'%OH[-1])
#     print('OOH=%.2f'%OOH[-1])
#     print(t)
#     c_x.append(X[-1])
#     c_o.append(O[-1])
#     c_oh.append(OH[-1])
#     c_ooh.append(OOH[-1])
    
# fig,ax=plt.subplots(1,1)
# ax.set_xlabel('$U_{RHE}$')
# ax.set_ylabel('Coverage (a.u.)')
# plt.xlim(0, 1)
# plt.ylim(-0.1, 1.1)
# plt.plot(U, c_x, label='M',linewidth=1.0,linestyle='solid')
# #plt.scatter(U, c_x,linewidth=0.2)
# plt.plot(U, c_oh, label='*OH-M',linewidth=1.0,linestyle='solid')
# #plt.scatter(U, c_oh,linewidth=0.2)
# plt.plot(U, c_o, label='*O-M',linewidth=1.0,linestyle='solid')
# #plt.scatter(U, c_o,linewidth=0.2)
# plt.legend()
# plt.show()