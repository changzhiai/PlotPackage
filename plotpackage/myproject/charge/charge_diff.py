# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 14:33:10 2021

@author: changai
"""

from ase.calculators.vasp import VaspChargeDensity
from ase.io import write
from mayavi import mlab
import matplotlib.pyplot as plt

spin_cut_off = 0.1
density_cut_off = 0.01

rotation = '24x, 34y, 14z'
# rotation = '0x, 0y, 0z'


vchg = VaspChargeDensity('CHGDIFF.vasp')
atoms = vchg.atoms[0]
chg = vchg.chg[0]
print(atoms.positions[:,0])
atoms_x = atoms.positions[:,0]
atoms_y = atoms.positions[:,1]
atoms_z = atoms.positions[:,2]

# plt.figure()
# plt.contourf(atoms_x, atoms_y, atoms_z, vchg, cmap=plt.cm.hot)
mlab.contour3d(atoms_x, atoms_y, atoms_z, chg)