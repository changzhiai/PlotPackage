# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 00:31:10 2021

@author: changai
"""

from plotpackage.lib.io import read_excel, read_csv
from plotpackage.lib.freeenergy import EnergyDiagram
import matplotlib.pyplot as plt

#with barriers
class CO2RRFEDplot:
    def __init__(self, stepsnames, obsername, X_, figname):
        # plot parameters
        self.stepsNames = stepsnames
        self.observationName = obsername
        self.X = X_
        self.figName = figname
        
        self.axFree = None
        self.figFree = None
        #self.stepsNames, self.observationName, X = read_excel(filename, sheet, min_col, max_col, min_row, max_row) #load excel data
        #self.stepsNames, self.observationName, X = read_csv(filename, , min_col, max_col) #load csv data
        print('auto loaded stepsName: ', self.stepsNames)
        print('auto loaded obserName: ', self.observationName)
        print('auto loaded data: \n', self.X)
        
        delNames = []
        for i in range(int(len(self.stepsNames))):
            if i % 2 != 0:
                delNames.append(self.stepsNames[i])
        self.realSteps = list(set(self.stepsNames).difference(set(delNames)))
        
        self.colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g']
        #colorList = ['gray', 'brown', 'orange', 'olive', 'green', 'cyan', 'blue', 'purple', 'pink', 'red']
        #colorList = ['k', 'g', 'r', 'b', 'c', 'm', 'y', 'brown', 'pink', 'gray', 'orange', 'purple', 'olive']
        self.realSteps = ['* + CO2', '*HOCO', '*CO', '* + CO']  #reload step name for CO2RR
        #realSteps = ['* + $H^+$', '*H', '* + 1/2$H_2$',]  #reload step name for HER
        #self.observationName = ["Pure", "Ni", "Co", "V", "Cr", "Mn", "Fe", "Pt"]  #reload specis name

        print('reload:', self.realSteps)
        print('reload:', self.observationName, '\n')
        
        self.diagram = EnergyDiagram()
        count = 0
        for specis in range(len(self.observationName)):
            for step in range(len(self.realSteps)):
                count += 1
                if step == 0:
                    self.diagram.pos_number = 0
                
                energy_col = 2 * step        
                self.diagram.add_level(self.X[specis][energy_col], color = self.colorList[specis])
        
                if count % (len(self.realSteps)) != 0:
                    if self.X[specis][energy_col+1] == 0: #plot general link line if TS energy is equle to 0
                        self.diagram.add_link(count-1, count, color = self.colorList[specis])
                        #print(count-1)
                    else: #plot ts barrier
                        self.diagram.add_barrier(start_level_id=count-1, barrier=self.X[specis][energy_col+1]+self.X[specis][energy_col], end_level_id=count, color = self.colorList[specis]) #add energy TS barriers
    
    def add_link(self, start_id=None, end_id=None, color='k', linestyle='--', linewidth=1):
        if start_id != None and end_id != None:  #pos starts from 0
            self.diagram.add_link(start_id, end_id, color, linestyle, linewidth)
    
    def remove_link(self, start_id=None, end_id=None):
        if start_id != None and end_id != None:
            self.diagram.remove_link(start_id, end_id)
            
    def add_ts(self, start_id, barrier, end_id, color='k', linestyle='--', linewidth=1):
        if start_id != None and end_id != None:
            specis = int(start_id) // len(self.realSteps)
            energy_col = 2 * int(start_id) % len(self.realSteps)
            real_barrier = self.X[specis][energy_col] + barrier
            self.diagram.add_barrier(start_id, real_barrier, end_id, color, linestyle, linewidth)
    
    def remove_ts(self, start_id=None, end_id=None):
        if start_id != None and end_id != None:
            self.diagram.remove_barrier(start_id, end_id)
        
    def plot(self, title=''):
        figFree = plt.figure(figsize=(8,6), dpi = 300)
        axFree = figFree.add_subplot(111)                 
        # diagram.add_barrier(start_level_id=0, barrier=2, end_level_id=1) #add energy barriers
        #diagram.plot(xtickslabel = self.stepsNames, stepLens=len(self.stepsNames), ax=axFree) # this is the default ylabel
        pos = self.diagram.plot(xtickslabel = self.realSteps, stepLens=len(self.realSteps), ax=axFree) # this is the default ylabel
        #add legend
        for specis in range(len(self.observationName)):
            plt.hlines(0.1, pos[0], pos[0], color=self.colorList[specis], label= self.observationName[specis])
        plt.legend(fontsize=12)
        plt.title(title, fontsize=14)
        
        plt.show()
        figFree.savefig(self.figName)
    
        