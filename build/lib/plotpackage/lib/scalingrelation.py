# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 01:06:31 2021

@author: changai
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

class ScalingRelationPlot:
    def __init__(self, descriper1, descriper2, obsername, figname):
        # plot parameters
        self.descriper1 = descriper1
        self.descriper2 = descriper2
        self.observationName = obsername
        self.figName = figname
        
    def plot(self, ax: plt.Axes = None, dotcolor='black', linecolor='red', save = False, xlabel='*HOCO', ylabel='*CO', title='', text=''):                
        # print('scaling relation:')
        # print('x axis' + '(' + xlabel + '): ', self.descriper1)
        # print('y axis' + '(' + ylabel + '): ', self.descriper2, '\n')
        
        #plot data points
        if not ax:
            fig = plt.figure(figsize=(8, 6), dpi = 300)
            ax = fig.add_subplot(111)
        # Otherwise register the axes and figure the user passed.
        else:
            self.ax = ax
            # self.fig = ax.figure

        #fig = plt.figure(figsize=(8, 6), dpi = 300)
        #plt.plot(self.descriper1, self.descriper2, 's', color='black')  #plot dots
        
        # add element tags
        if isinstance(dotcolor, dict)==True:
            for i, name in enumerate(self.observationName):
                plt.plot(self.descriper1[i], self.descriper2[i], 's', color=dotcolor[name])  #plot dots
                plt.annotate(name, (self.descriper1[i], self.descriper2[i]+0.005), color=dotcolor[name], fontsize=14, horizontalalignment='center', verticalalignment='bottom')
        else:
            plt.plot(self.descriper1, self.descriper2, 's', color=dotcolor)  #plot dots
            for i, name in enumerate(self.observationName):
                plt.annotate(name, (self.descriper1[i], self.descriper2[i]+0.005), color=dotcolor, fontsize=14, horizontalalignment='center', verticalalignment='bottom')
                

        # plt.plot(self.descriper1, self.descriper2, 's', color=dotcolor)  #plot dots
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        ax.yaxis.set_label_coords(-0.12, 0.5)
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.margins(y=0.08)
        plt.title(title, fontsize=14)
        plt.text(0.05, 0.93, text, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes, fontsize=14, fontweight='bold')        
        
        #get current axis object and change format
        #ax = fig.gca()
        ax.tick_params(labelsize=12) #tick label font size
        for axis in ['top','bottom','left','right']:
            ax.spines[axis].set_linewidth(1.2) #linewith of frame
        
        #linear fiting and plot linear line
        m, b = np.polyfit(self.descriper1, self.descriper2, 1)
        handleFit = plt.plot(self.descriper1, m * self.descriper1 + b, linewidth=2, color=linecolor)
        #handleFit = plt.plot(self.descriper1, m * self.descriper1 + b, linewidth=2, color='red')
        
        #add r2 tag
        from sklearn.metrics import r2_score
        model = np.array([m, b])
        predict = np.poly1d(model)
        r2 = r2_score(self.descriper2, predict(self.descriper1))
        r2 = np.round(r2, 2)
        m = np.round(m, 2)
        b = np.round(b, 2)
        #plt.text(0.85, 0.3, 'R2 = {}'.format(r2), fontsize=14)
        plt.legend(handles = handleFit, labelcolor=linecolor, labels = ['$R^2$ = {}\ny = {} + {} * x '.format(r2, b, m)], loc="lower right", handlelength=0, fontsize=14)
        print('r2:', r2)
        
        #save figure
        if save == True: 
            plt.show()
            fig.savefig(self.figName)
        
        # return fig