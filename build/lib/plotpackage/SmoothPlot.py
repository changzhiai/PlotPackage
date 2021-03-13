# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 23:23:10 2021

@author: changai
"""

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np



x = [1, 2.5, 4]
y = [1, 5, 0]

f = interp1d(x, y, kind='quadratic')

x_interpol = np.linspace(1, 4, 1000)
y_interpol = f(x_interpol)

plt.plot(x_interpol, y_interpol)
plt.show()