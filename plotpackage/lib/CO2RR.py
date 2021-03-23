# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 00:31:10 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.freeenergy import EnergyDiagram
import matplotlib.pyplot as plt

class CO2RRFEDplot:
    def __init__(self, stepsnames, obsername, X_, figname):
        # plot parameters
        self.stepsNames = stepsnames
        self.observationName = obsername
        self.X = X_
        self.figName = figname
        
    def plot(self, title=''):
        #self.stepsNames, self.observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
        #self.stepsNames, self.observationName, X = read_csv(filename, , min_col, max_col) #load csv data
        print('auto loaded stepsName: ', self.stepsNames)
        print('auto loaded obserName: ', self.observationName)
        print('auto loaded data: \n', self.X)
        
        colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g']
        #colorList = ['gray', 'brown', 'orange', 'olive', 'green', 'cyan', 'blue', 'purple', 'pink', 'red']
        #colorList = ['k', 'g', 'r', 'b', 'c', 'm', 'y', 'brown', 'pink', 'gray', 'orange', 'purple', 'olive']
        self.stepsNames = ['* + CO2', '*HOCO', '*CO', '* + CO']  #reload step name for CO2RR
        #self.stepsNames = ['* + $H^+$', '*H', '* + 1/2$H_2$',]  #reload step name for HER
        #self.observationName = ["Pure", "Ni", "Co", "V", "Cr", "Mn", "Fe", "Pt"]  #reload specis name
        print('reload:', self.stepsNames)
        print('reload:', self.observationName, '\n')
        
        
        diagram = EnergyDiagram()
        count = 0
        for specis in range(len(self.observationName)):
            for step in range(len(self.stepsNames)):
                count += 1
                if step == 0:
                    diagram.pos_number = 0
                    
                diagram.add_level(self.X[specis][step], color = colorList[specis])
        
                if count % (len(self.stepsNames)) != 0:
                    diagram.add_link(count-1, count, color = colorList[specis])
                
        figFree = plt.figure(figsize=(8,6), dpi = 300)
        axFree = figFree.add_subplot(111)
                
        #diagram.add_barrier(start_level_id=1, barrier=1, end_level_id=2) #add energy barriers
        diagram.plot(xtickslabel = self.stepsNames, stepLens=len(self.stepsNames), ax=axFree) # this is the default ylabel
        
        #add legend
        for specis in range(len(self.observationName)):
            plt.hlines(0.1, 0.5, 0.5, color=colorList[specis], label= self.observationName[specis])
        plt.legend(fontsize=12)
        plt.title(title, fontsize=14)
        
        plt.show()
        figFree.savefig(self.figName)