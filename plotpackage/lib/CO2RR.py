# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 00:31:10 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.freeenergy import EnergyDiagram
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

class CO2RRFEDplot:
    def __init__(self, stepsnames, obsername, X_, figname):
        # plot parameters
        self.stepsNames = stepsnames
        self.observationName = obsername
        self.X = X_
        self.figName = figname
        
        # self.axFree = None
        # self.figFree = None
        
        #self.stepsNames, self.observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
        #self.stepsNames, self.observationName, X = read_csv(filename, , min_col, max_col) #load csv data
        print('auto loaded stepsName: ', self.stepsNames)
        print('auto loaded obserName: ', self.observationName)
        print('auto loaded data: \n', self.X)
        
        # self.colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g', 'crimson', 'brown', \
        #                   'teal', 'thistle', 'y', 'tan', 'navy', 'wheat', 'gold', 'lightcoral', 'silver', 'violet', 'turquoise', 'seagreen', 'tan', \
        #                   'k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g', 'pink', 'brown',\
        #                   'k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g', 'pink', 'brown']
        self.colorList = {'PdH': 'black', 'Pure': 'black', 'Ti': 'red', 'Pd': 'black', 'Sc': 'blue', 'V': 'orange', 'Cr': 'wheat', 'Mn': 'green', \
                          'Fe': 'lightgray', 'Co': 'deepskyblue', 'Ni': 'pink', 'Cu': 'purple', 'Zn': 'olive', 'Y': 'cyan', 'Zr': 'lime', \
                          'Nb': 'yellow', 'Mo': 'navy', 'Ru': 'magenta', 'Rh': 'brown', 'Ag': 'lightseagreen', 'Cd': 'steelblue', 'Hf': 'slateblue', \
                          'Ta': 'violet', 'W': 'deeppink', 'Re': 'palevioletred'}
        #colorList = ['gray', 'brown', 'orange', 'olive', 'green', 'cyan', 'blue', 'purple', 'pink', 'red']
        #colorList = ['k', 'g', 'r', 'b', 'c', 'm', 'y', 'brown', 'pink', 'gray', 'orange', 'purple', 'olive']
        #self.stepsNames = ['* + CO2', '*HOCO', '*CO', '* + CO']  #reload step name for CO2RR
        #self.stepsNames = ['* + $H^+$', '*H', '* + 1/2$H_2$',]  #reload step name for HER
        #self.observationName = ["Pure", "Ni", "Co", "V", "Cr", "Mn", "Fe", "Pt"]  #reload specis name
        print('reload:', self.stepsNames)
        print('reload:', self.observationName, '\n')
        
        self.diagram = EnergyDiagram()
        count = 0
        for i, specis in enumerate(self.observationName):
            for step in range(len(self.stepsNames)):
        # for specis in range(len(self.observationName)):
        #     for step in range(len(self.stepsNames)):
                count += 1
                if step == 0:
                    self.diagram.pos_number = 0
                
                self.diagram.add_level(self.X[i][step], color = self.colorList[specis])
        
                if count % (len(self.stepsNames)) != 0:
                    self.diagram.add_link(count-1, count, color = self.colorList[specis])
    
    def add_link(self, start_id=None, end_id=None, color='k', linestyle='--', linewidth=1):
        if start_id != None and end_id != None:  #pos starts from 0
            self.diagram.add_link(start_id, end_id, color, linestyle, linewidth)

    def remove_link(self, start_id=None, end_id=None):
        if start_id != None and end_id != None:
            self.diagram.remove_link(start_id, end_id)
    
    def plot(self, ax: plt.Axes = None, title='', save = False, legandSize = 14, text='', ratio=1.6181):
        if not ax:
            figFree = plt.figure(figsize=(8, 6), dpi = 300)
            axFree = figFree.add_subplot(111)
        # Otherwise register the axes and figure the user passed.
        else:
            axFree = ax
            # self.fig = ax.figure
           
        #diagram.add_barrier(start_level_id=1, barrier=1, end_level_id=2) #add energy barriers
        pos = self.diagram.plot(xtickslabel = self.stepsNames, stepLens=len(self.stepsNames), ax=axFree, ratio=ratio) # this is the default ylabel
        
        # add legend
        # for specis in range(len(self.observationName)):
        for i, specis in enumerate(self.observationName):
            plt.hlines(0.1, pos[0], pos[0], color=self.colorList[specis], label= specis)
        plt.legend(fontsize=legandSize)
        plt.title(title, fontsize=14)
        plt.text(0.04, 0.93, text, horizontalalignment='left', verticalalignment='center', transform=axFree.transAxes, fontsize=14, fontweight='bold')        
        axFree.yaxis.set_label_coords(-0.1, 0.5)
        axFree.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
        #save figure
        if save == True: 
            plt.show()
            figFree.savefig(self.figName, dpi=300, bbox_inches='tight')
        
        # return figFree
