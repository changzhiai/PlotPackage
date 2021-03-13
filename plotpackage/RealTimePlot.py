# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 21:24:24 2021

@author: changai
"""

import time
import psutil
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()


i = 0
x, y = [], []

while True:
    x.append(i)
    y.append(psutil.cpu_percent())
    
    ax.plot(x, y, color='b')
    fig.canvas.draw()  #re-draw the current figure
    plt.pause(0.05)

    ax.set_xlim(left=max(0, i-50), right=i+50) #adjust x axis

    time.sleep(0.95)
    i += 1
    

