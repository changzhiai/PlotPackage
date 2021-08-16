# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 14:42:44 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.figsmetadata import FigsMetaData
import matplotlib.pyplot as plt
import numpy as np

filename = '../data/formation_energy.xlsx'
#change it for excel and csv; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #1st column in excel
max_col = 7 #5th column in excel

#change it only for excel
sheet = 'Selectivity' #Sheet1 by defaut
# sheet = 'Formation Energy' #Sheet1 by defaut
min_row = 1 #1st column in excel
max_row = 17 #9st column in excel

#saved figure name
figName1 = '../pictures/Formation_energy_new_' + sheet + '.jpg'  #free energy diagram name

############ plot free energy diagram ###############
colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g']
typeNames, observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
#stepsNames, observationName, X = read_csv(filename, , min_col, max_col) #load csv data

fig = plt.figure(figsize=(8, 6), dpi = 300)
x = np.arange(0,len(observationName),1)

marker = ['o', '^', '<', '>', 'v', 's', 'd', '.', ',', 'x', '+']
for i in range(len(typeNames)):    
    plt.plot(x, X[:,i], 'o', color=colorList[i])  #plot dots
    # plt.plot(x, X[:,i], marker[i], color=colorList[i])  #plot dots
    
plt.legend(typeNames, framealpha=0.5, fontsize=12)
plt.axhline(y=0, color='r', linestyle='--')

# plt.xlim([-10, 8])
plt.ylim([-2.5, 2.5])
plt.xlabel('Doping elements', fontsize=16)
# plt.ylabel('Formation energy (eV/atom)', fontsize=14)
plt.ylabel('ΔG(HOCO*)-ΔG(H*)', fontsize=16)
plt.title(sheet, fontsize=16)
ax = fig.gca()
ax.set_xticks(x)
ax.set_xticklabels(observationName)

ax.tick_params(labelsize=14) #tick label font size
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2) #linewith of frame
    
    
# plt.arrow(x=16, y=0, dx=0, dy=2, width=.4, head_width=0.8, head_length=0.3) 
# plt.annotate('HER', xy = (16.5, 1), rotation=90, fontsize=14)

# plt.arrow(x=16, y=0, dx=0, dy=-2, width=.4, head_width=0.8, head_length=0.3) 
# plt.annotate('CO$_2$RR', xy = (16.5, -1.5), rotation=90, fontsize=14)
import matplotlib.transforms
import matplotlib.path
from matplotlib.collections import LineCollection

def rainbowarrow(ax, start, end, cmap="viridis", n=50,lw=3):
    cmap = plt.get_cmap(cmap,n)
    # Arrow shaft: LineCollection
    x = np.linspace(start[0],end[0],n)
    y = np.linspace(start[1],end[1],n)
    points = np.array([x,y]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-1],points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, linewidth=lw)
    lc.set_array(np.linspace(0,1,n))
    ax.add_collection(lc)
    # Arrow head: Triangle
    tricoords = [(0,-0.4),(0.5,0),(0,0.4),(0,-0.4)]
    angle = np.arctan2(end[1]-start[1],end[0]-start[0])
    rot = matplotlib.transforms.Affine2D().rotate(angle)
    tricoords2 = rot.transform(tricoords)
    tri = matplotlib.path.Path(tricoords2, closed=True)
    ax.scatter(end[0],end[1], c=1, s=(2*lw)**2, marker=tri, cmap=cmap,vmin=0)
    ax.autoscale_view()

rainbowarrow(ax, (16,0), (16, 2), cmap='Reds', n=50, lw=9) 
plt.annotate('HER', xy = (16.2, 1), rotation=90, fontsize=14)

rainbowarrow(ax, (16,0), (16, -2), cmap='Reds', n=50, lw=9) 
plt.annotate('CO$_2$RR', xy = (16.2, -1.5), rotation=90, fontsize=14)
# plt.arrow(x=16, y=0, dx=0, dy=-2, width=.4, head_width=0.8, head_length=0.3) 
# plt.annotate('CO$_2$RR', xy = (16.5, -1.5), rotation=90, fontsize=14)

plt.show()


fig.savefig(figName1)


#add metadata into pictures
figNames = [figName1]
fmd = FigsMetaData(figNames, filename, sheet, min_col, max_col, min_row, max_row)
fmd.add_metadata()