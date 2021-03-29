# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 21:59:06 2021

@author: changai
"""
from plotpackage.lib.io import read_two_column_file, read_two_column_PDOS
import matplotlib.pyplot as plt

colorList = ['k', 'k', 'lime', 'lime', 'r', 'r', 'b', 'b', 'darkcyan', 'darkcyan', 'cyan', 'cyan', 'olive', 'olive', 'magenta', 'magenta', 'pink', 'pink', 'gray', 'orange', 'purple', 'g']

# #plot two columns
# filename = './data/dos.txt' #just regular two column data
# x, y = read_two_column_file(filename)
# fig = plt.figure(figsize=(8, 6), dpi = 300)
# plt.plot(x, y, color='k')  #plot line
# #print(x)

# set for PDOS
filename = '../data/d-band.txt' #with blink lines
threshold = 1000
scope = 4

#plot multi lines using data in two columns
fig = plt.figure(figsize=(8, 6), dpi = 300)
for i in range(scope):
    x, y = read_two_column_PDOS(filename, i, threshold) #read every threshold lines
    #print(x)
    plt.plot(x, y, color=colorList[i])  

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

M=2
fig = plt.figure(figsize=(8, 6), dpi = 300)
for m1 in range(M):
    for m2 in range(M):
        plt.subplot(M, M, m1*M + m2 + 1)
        i = m1*M + m2
        x, y = read_two_column_PDOS(filename, i, threshold) #read every threshold lines
        plt.plot(x, y, color=colorList[i])
        
        plt.title('', fontsize=14)
        plt.xlim([-10, 8])
        plt.ylim([-300, 400])
        ax = fig.gca()
        ax.tick_params(labelsize=12) #tick label font size
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(1.2) #linewith of frame

        if m1==M-1:
            plt.xlabel('Energy (eV)', fontsize=14)
        else:
            plt.xticks([])
        if m2==0:
            plt.ylabel('PDOS', fontsize=14)
        else:
            plt.yticks([])

fig.tight_layout()

fig.suptitle('dos', x = 0.55, y=1.01, fontsize=16)
plt.show()