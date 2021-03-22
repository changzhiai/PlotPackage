# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 21:50:27 2021

@author: changai
"""

from plotpackage.lib.io import read_two_column_file
import matplotlib.pyplot as plt

colorList = ['k', 'k', 'lime', 'lime', 'r', 'r', 'b', 'b', 'darkcyan', 'darkcyan', 'cyan', 'cyan', 'olive', 'olive', 'magenta', 'magenta', 'pink', 'pink', 'gray', 'orange', 'purple', 'g']

#plot two columns
filename = '../data/dos.txt' #just regular two column data
x, y = read_two_column_file(filename)
fig = plt.figure(figsize=(8, 6), dpi = 300)
plt.plot(x, y, color='k')  #plot line
#print(x)

plt.xlim([-10, 8])
plt.ylim([-300, 400])
plt.xlabel('Energy (eV)', fontsize=14)
plt.ylabel('PDOS', fontsize=14)
plt.title('dos', fontsize=14)
ax = fig.gca()
ax.tick_params(labelsize=12) #tick label font size
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2) #linewith of frame
plt.show()