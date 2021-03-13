# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 21:59:06 2021

@author: changai
"""
import matplotlib.pyplot as plt

# set for PDOSr
threshold = 1000
scope = 4

def Read_Two_Column_File(file_name):  #for no blank lines case
    file = open(file_name, 'r') 
    lines = file.readlines()
    x = []
    y = []
    for line in lines:
        print(line)
        p = line.split()
        x.append(float(p[0]))
        y.append(float(p[1]))
    return x, y

def Read_Two_Column_PDOS(l, file_name): #for blank case like PDOS
    x = []
    y = [] 
    file = open(file_name, 'r') 
    lines = file.readlines()
    for line in lines[threshold*l+l:threshold*(l+1)+l]:
        print(line)
        p = line.split()
        x.append(float(p[0]))
        y.append(float(p[1]))
    return x, y

# x, y = Read_Two_Column_PDOS('./d-band.txt')
# print(x)
colorList = ['k', 'k', 'lime', 'lime', 'r', 'r', 'b', 'b', 'darkcyan', 'darkcyan', 'cyan', 'cyan', 'olive', 'olive', 'magenta', 'magenta', 'pink', 'pink', 'gray', 'orange', 'purple', 'g']
fig = plt.figure(figsize=(8, 6), dpi = 300)
for i in range(scope):
    x, y = Read_Two_Column_PDOS(l = i, file_name = './d-band.txt')
    print(x)
    plt.plot(x, y, color=colorList[i])  #plot dots

plt.xlim([-10, 8])
plt.ylim([-300, 400])
plt.xlabel('Energy (eV)', fontsize=14)
plt.ylabel('PDOS', fontsize=14)
ax = fig.gca()
ax.tick_params(labelsize=12) #tick label font size
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2) #linewith of frame
plt.show()