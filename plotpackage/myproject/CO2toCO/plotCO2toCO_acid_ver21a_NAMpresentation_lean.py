import numpy as np
from numpy import exp, log
from ase.units import kB
#from CO2toCO_alkaline10a import CO2toCO
from CO2toCO_acid import CO2toCO
#from CO2red_data import Au_Hori_CO, Au_IC_CO, Au3Ag_IC_CO, Ag3Au_IC_CO, Cu_Hori_CO

hplanck = 4.135669e-15 # eV s
texts = ['Cu', 'Au', 'Ag', 'Pt', 'Pd', 'Ni', 'Rh'] #, 'FeVco', 'FeMoco'] 
E_COOH_sel = np.array([0.3155624, 0.6663682, 0.7761599, -0.5210433, -0.0414823, -0.3107622, -0.5689026]) #, 0.869054 ,0.986972 ])
E_CO_sel = np.array([-0.6758434, -0.3918677, -0.1812588, -1.9719458, -1.8069736, -1.712983, -1.9257488]) #, -0.517252, -0.458841])

texts_Cu = ['Cu-4', 'Cu-2', 'Cu', 'Cu+2', 'Cu+4', 'Cu100', 'Cu111'] 
E_COOH_Cu = np.array([ 0.4573029, 0.4239818, 0.3907024, 0.3530644, 0.3158175, 0.5386893, 0.8069658])
E_CO_Cu = np.array([ -0.6435299, -0.6403733, -0.6518864, -0.661628, -0.6664611, -0.5603989, -0.4421704])

texts_Au = ['Au-4', 'Au-2', 'Au', 'Au+2', 'Au+4'] 
E_COOH_Au = np.array([0.808491, 0.7666629, 0.7173317, 0.729899, 0.7100136])
E_CO_Au = np.array([-0.2926736, -0.309032, -0.35694, -0.420279, -0.4264837])

texts_100 = np.array(['Ag', 'Au', 'Cu', 'Ni', 'Pd', 'Pt', 'Rh'])
E_COOH_100 = np.array([0.8407948, 0.808538, 0.5142602, -0.1908111, 0.181098, -0.108439, -0.3713502])
E_CO_100 = np.array([-0.1182908, -0.31399, -0.5625809, -1.6648072, -1.6445583, -1.8036744, -1.8754177])

texts_111 = np.array(['Ag', 'Au', 'Cu', 'Ni', 'Pd', 'Pt', 'Rh'])
E_COOH_111 = np.array([1.0749761, 0.957277, 0.7659526, 0.193338, 0.332705, 0.093657, -0.1148555])
E_CO_111 = np.array([0.0049459, -0.035054, -0.5368441, -1.6231988, -1.73272, -1.5234243, -1.7525061])

# surface roughness
if 0:
    SR = {'Cu': (1.+2.+4.)/3.,
          'Ag': 3.,
          'Au': 8.,
          }
elif 1: #  no roughness correction
    SR = {'Cu': 1.,
          'Ag': 1.,
          'Au': 1.,
          }

N_sel = len(E_CO_sel)


#T0 = 18.5 + 273.15
T0 = 18.0 + 273.15
#T0 = 25 + 273.15
tof2j = 222 *.05 * 2 # convert TOF (site/s) to j (micro A / cm2) (220 from Au(111) surface charge densty, 5% steps, 2e process) 
tof2j_CODH = 2 * 2 * 0.46e-12 * 6.022e23 * 1.602e-19 * 1e6 # convert TOF to j (micro A/cm2) from 0.46 pmol / cm2

print(tof2j, tof2j_CODH)

nu_e_0 = kB * T0 / hplanck
nu_c_0 = 1.e13

# linear relation for E_COOH vs E_CO, wth shift of C reference from C to CO2 
alpha_CO2 = 0.73 
beta_CO2 = 1.82 - 0.90 

# correct the reversible potential
ddG_TD = 0. #-0.15 #XXX implement for ECOOH as well?

if 1: # old corrections
    # correction for change of 'standard pressure' of CO vs aap paper. 
    ddGpCO = - kB * (18.5+273.15) * log( 5562. / 101325. ) # Do not change this T!
    # Free energy correction for COOH formation
    ddG_COOH = 0.542 - (0.31 +0.1 -0.65) 

    # CO2 backbone correction (IS), water stabilization of 
    ddG_COOH += -0.25 - 0.45 

    # Free energy correction for COOH* + 1/2 H2(g) -> CO* + H2O(g)
    ddG_CO = 0.115 + 0.58 + 0.1 - 0.65 - ( 0.542 +0.27 +0.09 -0.39)
    ddG_CO += -0.1 - ( - 0.25) # solvent stabilzation of CO and COOH
    # Correction when calculating COOH* -> CO* because E_CO is calculated vs. CO(g) and not CO2(g) 
    # Natural place to correct for CO reversible potential being off?
    #ddE_CO = 0.879
    dE_tot = 0.879 + ddG_TD 

    # Free energy correction for CO adsorption
    ddG_COads = 0.115 - ( 0.14 +0.09 -0.67 +ddGpCO)
    # Change in ZPE upon adsorption
    dZPE_COads = 0.192 - 0.14
    # stabilization from the solvent
    ddG_COads += - 0.1
if 1: # corrections as written in the paper
    ddG1 = 0.80
    ddG2 = -0.38
    ddG3 = -0.48
    ddE_COOH_hb = -0.25
    ddE_CO_hb = -0.10
    ddE_CO2_bb = 0.45 # CO2 backbone

cH2O = 1. # 1.e3 / (16. + 2 * 1.008)
Kw = 1.e-14
if 0:
    prefix = 'tc05b_acid_in_neutral_'
    cHp0 = 10.**(-7.5)
    cOHm0 = Kw/cHp0
    UHER0 = URHE0 = kB * T0 * np.log(cHp0)   # introduced to shift the plotted potential window to the relevant range w
if 1:  # prefix may be overwritten later ...
    prefix = 'tc05b_acid_in_acid_'
    #prefix = 'tc05_RDS2_acid_in_acid_'
    cHp0 = 10.**(-0.)
    cOHm0 = Kw/cHp0
    UHER0 = URHE0 = kB * T0 * np.log(cHp0)   # introduced to shift the plotted potential window to the relevant range w
DeltaG_H = -kB * T0 * np.log(cHp0)  # free energy correction due to non
DeltaG_OH= 0. # kB * T0 * np.log(cOHm0) # standard OH concentration (only
                                   # used when plotting DeltaG)


if 1: # new in model 13a ?    
    if 0:
        prefix = 'Model1/tc05b_acid_in_acid_'
        prefix = 'Model1_ExpComp/'
        Gact0 = Gact1 = Gact2 = 0.475
        tc0 = tc1 = tc2 = 0.5
        betaBE0 = 0.5 # 0.5 # 
        nu_c_0 = 1.e13
    elif 1:
        #prefix = 'Model1_NAM23/tc05b_acid_in_acid_'
        prefix = 'Model1_Proposal/tc05b_acid_in_acid_'
        Gact0 = Gact1 = Gact2 = 0.475
        tc0 = tc1 = tc2 = 0.5
        betaBE0 = 0.5 # 0.5 # 
        nu_c_0 = 1.e13
    A_act1 = np.exp( - Gact1 / ( kB * T0 ) ) # 
    A_act2 = np.exp( - Gact2 / ( kB * T0 ) ) # electrochemical prefactor, fitting
    G_1act_cap = -Gact1
    G_2act_cap = -Gact2

# The free energy corresponding to the concentration of CO2 assumed in the double layer
dGcorrX1 = 0. #- kB * T0 * np.log(1. * 3.5e-2 / cH2O ) 

# f = open(prefix+'out.txt', 'w')
# print >> f, 'Corrections:'
# print >> f, ddG_COOH , ddG1 +  ddE_COOH_hb - ddE_CO2_bb
# print >> f, ddG_CO, ddG2 + ddE_CO_hb - ddE_COOH_hb
# print >> f, -ddG_COads
# print >> f, "="*20
# print >> f, dGcorrX1, np.sqrt( 3.5e-2 / ( 1.e3 / (16. + 2 * 1.008) ) )
# print >> f, A_act1, A_act2 
# print >> f, nu_e_0 * A_act1
# print >> f, 'nu_0 : %.3g' % (nu_e_0)

def get_k1_n(nu, E_COOH, U, T=T0, tc=tc0):
    """ k1 'new'
    """
    beta = 1. / (kB * T)
    dG_rhe = E_COOH + ddG1 - ddE_CO2_bb +  ddE_COOH_hb
    Urev_rhe = -dG_rhe
    k1 = nu * A_act1 * exp( - max( ( U - Urev_rhe ) * tc, G_1act_cap) * beta )
    return k1

def get_K1_n(E_COOH, U, T=T0):
    """ K1 using COOH binding                                                               
    """
    beta = 1. / (kB * T)
    dG_rhe = E_COOH + ddG1 - ddE_CO2_bb +  ddE_COOH_hb
    K1 = exp( - (dG_rhe + 1.0 * U ) * beta )
    return K1

def COOH_CO_scaling(E_CO):
    return alpha_CO2 * E_CO + beta_CO2

def COOH_CO_scaling_facet(E_CO, facet='211'):
    if facet == '211':
        E_COOH = alpha_CO2 * E_CO + beta_CO2
    elif facet == '111':
        E_COOH = 0.552 * E_CO + 1.023084
    elif facet == '100':
        E_COOH = 0.589 * E_CO + 0.924084
    return E_COOH

def get_k1_s(nu, E_CO, U, T=T0, tc=tc1):
    """ k1 assuming scaling relation.
    """
    beta = 1. / (kB * T) 
    dG_rhe = ddG_COOH + (alpha_CO2 * E_CO + beta_CO2)
    dG_she = dG_rhe
    Urev_rhe = -dG_rhe 
    Urev_she = - dG_she + UHER0
    k1 = nu * A_act1 * exp( - max( ( U - Urev_rhe ) * tc, G_1act_cap) * beta ) 
    #print tc0, Urev_she
    #k1 = nu * A_act1 * exp( - max( ( U - Urev_she ) * tc, G_1act_cap) * beta ) 
    #dGw = - kB * T * np.log(Kw)
    #dG = 0. * Gact0 + ddG_COOH + dGw + (alpha_CO2 * E_CO + beta_CO2)
    #U0 = (1./tc - 1.) * dG - Gact0
    #k1 = nu * A_act1 * exp( - max( dG + ( U - U0 ) * tc, 0) * beta )
    return k1

def get_k1(nu, E_COOH, U, T=T0, tc=tc1):
    """ k1 using COOH binding (vs CO2 and H2)
    """
    beta = 1. / (kB * T) 
    dG_rhe = ddG_COOH + E_COOH
    dG_she = dG_rhe 
    Urev_rhe = -dG_rhe
    Urev_she = -dG_she + UHER0
    k1 = nu * A_act1 * exp( - max( ( U - Urev_rhe ) * tc, G_1act_cap) * beta ) 
    #k1 = nu * A_act1 * exp( - min( ( U - dG_she ) * tc, 0) * beta ) 
    #dGw =  - kB * T * np.log(Kw)
    #dG = 0. * Gact0 + ddG_COOH + E_COOH + dGw
    #U0 = (1./tc - 1.) * dG - Gact0
    #k1 = nu * A_act1 * exp( - max( dG + ( U - U0 ) * tc, 0) * beta )
    return k1

def get_k1_s(nu, E_CO, U, T=T0, tc=tc1, betaBE=betaBE0):
    """ k1 assuming scaling relation.
    """
    beta = 1. / (kB * T)
    dG_rhe = ddG_COOH + (alpha_CO2 * E_CO + beta_CO2)
    dG_she = dG_rhe
    Urev_rhe = -dG_rhe
    Urev_she = - dG_she + UHER0
    E_BEcorr = ( betaBE - tc ) * ( E_CO - E_CO_sel[1] ) * alpha_CO2
    k1 = nu * A_act1 * exp( - max( ( U - Urev_rhe + E_BEcorr) * tc, G_1act_cap) * beta )
    return k1

def get_k1(nu, E_COOH, U, T=T0, tc=tc0, betaBE=betaBE0):
    """ k1 using COOH binding (vs CO2 and H2).
    """
    beta = 1. / (kB * T)
    dG_rhe = ddG_COOH + E_COOH
    dG_she = dG_rhe
    Urev_rhe = -dG_rhe
    Urev_she = -dG_she + UHER0
    E_BEcorr = ( betaBE - tc ) * ( E_COOH - E_COOH_sel[1] )
    k1 = nu * A_act1 * exp( - max( ( U - Urev_rhe + E_BEcorr ) * tc, G_1act_cap) * beta )
    return k1

def get_Ga1_s(nu, E_CO, U, T=T0, tc=tc0):
    """ Activation energy for step 1
    """
    beta = 1. / (kB * T)
    dG = Gact0 + ddG_COOH + (alpha_CO2 * E_CO + beta_CO2)
    Gact = ( dG + U ) * tc
    return Gact

def get_Ga1(nu, E_COOH, U, T=T0, tc=tc0):
    """ Activation energy for step 1
    """
    beta = 1. / (kB * T)
    dG = Gact0 + ddG_COOH + E_COOH
    Gact =  ( dG + U ) * tc
    return k1

def get_K1_s(E_CO, U, T=T0):
    """ K1 assuming scaling
    """
    beta = 1. / (kB * T) 
    dG = ddG_COOH + (alpha_CO2 * E_CO + beta_CO2)
    K1 = exp( - ( dG + 1.0 * U ) * beta )
    return K1

def get_K1(E_COOH, U, T=T0):
    """ K1 using COOH binding
    """
    beta = 1. / (kB * T) 
    dG = ddG_COOH + E_COOH
    K1 = exp( - (dG + 1.0 * U ) * beta )
    return K1

def get_k2_s(nu, E_CO, U, T=T0, tc=tc2):
    """ k2 assuming scaling.
    """    
    beta = 1. / (kB * T) 
    dG_rhe = dE_tot + E_CO - (alpha_CO2 * E_CO + beta_CO2) + ddG_CO
    dG_she = dG_rhe
    Urev_rhe = -dG_rhe
    Urev_she = - dG_she + URHE0
    k2 = nu * A_act2 * exp( - max( ( U - Urev_rhe ) * tc, G_2act_cap) * beta )  
    return k2

def get_k2(nu, E_COOH, E_CO, U, T=T0, tc=tc2):
    """ k2 using COOH and CO energies.
    """    
    beta = 1. / (kB * T)  
    dG_rhe = dE_tot + E_CO - E_COOH + ddG_CO
    dG_she = dG_rhe
    Urev_rhe = -dG_rhe
    Urev_she = - dG_she + URHE0
    k2 = nu * A_act2 * exp( - max(( U - Urev_rhe ) * tc, G_2act_cap) * beta ) 
    return k2

def get_K2_s(E_CO, U, T=T0):
    """ K2 assuming scaling.
    """
    beta = 1. / (kB * T) 
    dG = dE_tot + E_CO - (alpha_CO2 * E_CO + beta_CO2) + ddG_CO 
    K2 = exp( - ( dG + 1.0 * U ) * beta ) 
    return K2

def get_K2(E_COOH, E_CO, U,  T=T0):
    """ K2 using COOH and CO binding.
    """
    beta = 1. / (kB * T) 
    dG = dE_tot + E_CO - E_COOH + ddG_CO
    K2 =  exp( - ( dG + 1.0 * U ) * beta ) 
    return K2

def get_k3_s(nu, E_CO, U, T=T0, tc=tc0):
    """ k3 assuming scaling.
    """
    beta = 1. / (kB * T) 
    dE = - dZPE_COads - E_CO
    dE = max(dE,0)
    k3 = nu * exp( - dE * beta )
    return k3

get_k3 = get_k3_s

def get_K3_s(E_CO, U, T=T0):
    """ K3 asumming scaling.
    """
    beta = 1. / (kB * T) 
    dG = -ddG_COads - E_CO 
    K3 = exp( - dG * beta )
    return K3

get_K3 = get_K3_s

def get_rates_s(nu_e, nu_c, E_CO, U, T=T0):
    """ Returns rate constants and equilibirum constants,
    """
    K1 = get_K1_s(E_CO, U, T=T)
    K2 = get_K2_s(E_CO, U, T=T)
    K3 = get_K3_s(E_CO, U, T=T)
    k1 = get_k1_s(nu_e, E_CO, U, T=T)
    k2 = get_k2_s(nu_e, E_CO, U, T=T)
    k3 = get_k3_s(nu_c, E_CO, U, T=T)
    return k1, K1, k2, K2, k3, K3

def get_rates(nu_e, nu_c, E_COOH, E_CO, U, T=T0):
    """ Returns rate constants and equilibirum constants,
    """
    K1 = get_K1(E_COOH, U, T=T)
    K2 = get_K2(E_COOH, E_CO, U, T=T)
    K3 = get_K3(E_CO, U, T=T)
    k1 = get_k1(nu_e, E_COOH, U, T=T)
    k2 = get_k2(nu_e, E_COOH, E_CO, U, T=T)
    k3 = get_k3(nu_c, E_CO, U, T=T)
    return k1, K1, k2, K2, k3, K3

if __name__ == '__main__':
    from matplotlib import rc
    rc('font', **{'family':'sans-serif','sans-serif':['Helvetica'], 'size':8})
    #rc('text', usetex=True)
    import pylab as pl
    import string
    SHOW = True
    U0 = -0.25-0.2# -0.20 #-0.23-0.2
    # print >> f,  'U RHE : %.2f' % (UHER0)
    # print >> f,  'exptl. DeltaG_act at 0.64mA/cm2 : %.3f' % (- kB * T0 * np.log((0.64/0.0222) / (nu_e_0) ) )
    # print >> f,  'exp(-Gact/(kBT)) : %.3g' % ( np.exp( -Gact0 / (kB * T0) ) )
    # print >> f,  'A : %.3g' % (nu_e_0 * A_act1)
    # print >> f,  'cH+ = %.3g' % (cHp0)
    # f.close()
    #cOHm0 = 1.e-7
    #cHp0  = 1.e-7
    #cOHm0 = 1.e-14
    #cHp0 = 1.    
    if 0: # test K1, K2, K3 using Cu(211) as an example
        E_COOH = 0.3155624
        E_CO = - 0.6758434 # CO ads energy
        #E_CO = - 0.3 # CO ads energy
        U = -0.0
        K1 = get_K1(E_COOH, U, T=T0)
        K2 = get_K2(E_COOH, E_CO, U, T=T0)
        K3 = get_K3(E_CO, U, T=T0)
        K1_s = get_K1_s(E_CO, U, T=T0)
        K2_s = get_K2_s(E_CO, U, T=T0)
        K3_s = get_K3_s(E_CO, U, T=T0)
        dG1, dG2, dG3 = -kB*T0*np.log(K1), -kB*T0*np.log(K2), -kB*T0*np.log(K3)
        dG1_s, dG2_s, dG3_s = -kB*T0*np.log(K1_s), -kB*T0*np.log(K2_s), -kB*T0*np.log(K3_s)
        print(ddG_COOH, ddG_CO, -ddG_COads)
        print(dG1, dG1 + dG2, dG1 + dG2 + dG3)
        print(dG1_s, dG1_s + dG2_s, dG1_s + dG2_s + dG3_s)
    if 1: # 2d volcano 
        U = U0 + UHER0
        nu_c = nu_c_0 #1e14
        nu_e = nu_e_0 #1.e8
        pCO2 = 1.
        pCO =  1.
        xH2O = 1.
        cHp = cHp0 #1.
        cOHm = cOHm0 # 1.e-14
        N = 20*4
        M = 30*4
        #E_COOH_e = np.linspace(-0.8, 0.95, M)
        #E_CO_e = np.linspace(-2.2, 0.2, N)
        E_COOH_e = np.linspace(-0.8, 1.45, M)
        E_CO_e = np.linspace(-2.2, 0.6, N)
        R = np.empty([M,N])
        Thetas = np.empty([M,N,3])
        #X = np.empty([N,N])
        jmax = 10.0e3 # exptl current plateau's at 10 mA/cm2 
        jmin = 0.1
        contours = np.linspace(np.log10(jmin), np.log10(jmax), 11) 
        for j, E_CO in enumerate(E_CO_e):
            for i, E_COOH in enumerate(E_COOH_e):
                k1, K1, k2, K2, k3, K3 = get_rates(nu_e, nu_c, E_COOH, E_CO, U, T=T0)
                #rm = CO2toCO(pCO2, pCO, xH2O, cHp, k1, K1, k2, K2, k3, K3)
                rm = CO2toCO(pCO2, pCO, xH2O, cOHm, k1, K1, k2, K2, k3, K3, T0)
                thetas, rates = rm.solve()
                rate = min(jmax, rates[0])
                rate = max(jmin, rate)
                R[i,j] = np.log10(rate)
                Thetas[i,j,:] = thetas        
        from pylabdefaults_square import *
        import pylab as pl
        f2 = pl.figure(1)
        pl.clf()
        pl.subplots_adjust(left=.16, bottom=.16, right=.96, top=.90)
        pl.hold(1)
        pl.contourf(E_CO_e, E_COOH_e, R, contours, cmap=pl.cm.jet)
        E_COOH_scaling = COOH_CO_scaling(E_CO_e)
        pl.plot(E_CO_e, E_COOH_scaling,'-k', lw=1)
        for i in range(N_sel): # elements
            pl.text(E_CO_sel[i], E_COOH_sel[i], texts[i], 
                    ha='center', va='center')
        if 1: # plot result from screening
            import pickle
            data = pickle.load(open('COOH_CO_data.pickle','r'))
            for surface_name, energies in data.items():
                if 1:
                    pl.text(energies['Eads_CO'], energies['Eads_COOH'], surface_name, 
                            fontsize=6,
                            ha='center', va='center')                
                if 1:
                    if 1: #surface_name[:-3] == 'Au3Cd':
                        if 1:
                            k1, K1, k2, K2, k3, K3 = get_rates(nu_e, nu_c, energies['Eads_COOH'], energies['Eads_CO'], U, T=T0)
                            #rm = CO2toCO(pCO2, pCO, xH2O, cHp, k1, K1, k2, K2, k3, K3)
                            rm = CO2toCO(pCO2, pCO, xH2O, cOHm, k1, K1, k2, K2, k3, K3, T0)
                            thetas, rates = rm.solve()
                            print(surface_name, rates[0])
                        pl.plot([energies['Eads_CO']], [energies['Eads_COOH']], '.k')
        pl.xlim([E_CO_e[0]+0.1, E_CO_e[-1]-0.1])
        pl.ylim([E_COOH_e[0]+0.1, E_COOH_e[-1]-0.1])
        pl.colorbar(ticks=np.arange(min(contours), max(contours), 0.5))
        pl.title(r'log$_{10}$(j/$\mu$Acm$^{-2}$)')
        pl.xlabel(r'$E_{\mathrm{CO}}$ (eV)')
        pl.ylabel(r'$E_{\mathrm{COOH}}$ (eV)')
        pl.savefig(prefix+'CO2toCO_rate_vs_COOH_CO.png', dpi=300)
        pl.show()
