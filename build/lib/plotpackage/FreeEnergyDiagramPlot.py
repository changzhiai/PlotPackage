# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 14:24:21 2021

@author: changai
"""

import numpy as np
import pandas as pd
from FreeEnergyDiagram import EnergyDiagram
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, plot, title, legend, xlabel, ylabel, show, tick_params
import xlrd

############only part needs to change##############
filename = '../data/HER.xlsx'
# #change it for both; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
# min_col = 12 #value 1 means it starts from 2rd(B) col in excel
# max_col = 16 #value 5 means it ends to 5th col (not including 6th col); 2-5(B-E) cols (1-4 in python)

# #change it only for excel
# sheet = 'doping-near-mag' #value 0 by defaut
# min_row = 33 #value 1 means it starts from 2rd row in excel
# max_row = 41 #value 9 means it ends to 9th rows (not including 10th row), or ignore it (1-8 in python)
# row_of_tag = min_row-1 #value 0 means 1st raw in excel;row number of tag
# col_of_tag = min_col-1 #value 0 means 1st(A) coloum in excel; coloum number of tag

#change it for both; ignore sheet, min_row, max_row, row_of_tag and col_of_ini_tag for csv
min_col = 1 #value 1 means it starts from 2rd(B) col in excel
max_col = 4 #value 5 means it ends to 5th col (not including 6th col); 2-5(B-E) cols (1-4 in python)

#change it only for excel
sheet = 'paral' #value 0 by defaut
min_row = 1 #value 1 means it starts from 2rd row in excel
max_row = 11 #value 9 means it ends to 9th rows (not including 10th row), or ignore it (1-8 in python)
row_of_tag = min_row-1 #value 0 means 1st raw in excel;row number of tag
col_of_tag = min_col-1 #value 0 means 1st(A) coloum in excel; coloum number of tag

#saved figure name
figName1 = '../pictures/FreeEnergy.jpg'  #free energy diagram name
figName2 = '../pictures/ScalingRelation.jpg' #scaling reation figure name

########### load excel data function###############

def read_excel(filename='./excel_data.xlsx'):  
    #doc = xlrd.open_workbook(filename).sheet_by_index(sheet)
    doc = xlrd.open_workbook(filename).sheet_by_name(sheet)
    stepsNames = doc.row_values(rowx=row_of_tag, start_colx=min_col, end_colx=max_col) # change 5 into xxx; obtain attributes name
    observationName = doc.col_values(col_of_tag, min_row, max_row) # change 9 into yyy; obtain observation name (0 coloum, 1-8 tags)

    X = np.empty((len(observationName),len(stepsNames)))
    for i in range(len(stepsNames)):
        X[:,i] = np.array(doc.col_values(i+1+col_of_tag ,1+row_of_tag,len(observationName)+1+row_of_tag)).T #raw data 
    return stepsNames, observationName, X
    

########### load csv data function#################

def read_csv(filename = './csv_data.csv'):  
    df = pd.read_csv(filename)
    raw_data = df.values
    
    cols = range(min_col, max_col) # change 5 into xxx
    stepsNames = np.asarray(df.columns[cols])  # obtain attributes name
    observationName = raw_data[:, 0] # obtain observation name
    
    X = raw_data[:, cols] # X = np.around(X.astype(np.double), decimals=3) # remain three decimal
    return stepsNames, observationName, X

############ plot free energy diagram ###############

stepsNames, observationName, X = read_excel(filename=filename) #load excel data
#stepsNames, observationName, X = read_csv(filename=filename) #load csv data
print('auto loaded stepsName: ', stepsNames)
print('auto loaded obserName: ', observationName)
print('auto loaded data: \n', X)

colorList = ['k', 'lime', 'r', 'b', 'darkcyan', 'cyan', 'olive', 'magenta', 'pink', 'gray', 'orange', 'purple', 'g']
#colorList = ['gray', 'brown', 'orange', 'olive', 'green', 'cyan', 'blue', 'purple', 'pink', 'red']
#colorList = ['k', 'g', 'r', 'b', 'c', 'm', 'y', 'brown', 'pink', 'gray', 'orange', 'purple', 'olive']
#stepsNames = ['* + CO2', '*HOCO', '*CO', '* + CO']  #reload step name for CO2RR
stepsNames = ['* + $H^+$', '*H', '* + 1/2$H_2$',]  #reload step name for HER
#observationName = ["Pure", "Ni", "Co", "V", "Cr", "Mn", "Fe", "Pt"]  #reload specis name
print('reload:', stepsNames)
print('reload:', observationName, '\n')


diagram = EnergyDiagram()
count = 0

figFree = plt.figure(figsize=(8,6), dpi = 300)
axFree = figFree.add_subplot(111)
for specis in range(len(observationName)):
    for step in range(len(stepsNames)):
        count += 1
        if step == 0:
            diagram.pos_number = 0
            
        diagram.add_level(X[specis][step], color = colorList[specis])
        #diagram.add_level(X[specis][step], stepsNames[step], color = colorList[specis])

        if count % (len(stepsNames)) != 0:
            diagram.add_link(count-1, count, color = colorList[specis])
            
#diagram.add_barrier(start_level_id=1, barrier=1, end_level_id=2) #add energy barriers
diagram.plot(xtickslabel = stepsNames, stepLens=len(stepsNames), ax=axFree) # this is the default ylabel

#add legend
for specis in range(len(observationName)):
    plt.hlines(1.2, 1, 1, color=colorList[specis], label= observationName[specis])
plt.legend(fontsize=12)

plt.show()
figFree.savefig(figName1)
assert False
############## plot scaling ralation ####################
descriper1 = (X[:, 1] - X[:, 0]).astype(float) #step2-step1
descriper2 = (X[:, 2] - X[:, 3]).astype(float) #step3-step4
print('scaling relation:')
print('descriper1: ', descriper1)
print('descriper2: ', descriper2, '\n')

#plot data points
fig = plt.figure(figsize=(8, 6), dpi = 300)
plt.plot(descriper1, descriper2, 's', color='black')  #plot dots
xlabel('*HOCO', fontsize=14)
ylabel('*CO', fontsize=14)
plt.margins(y=0.08)

#get current axis object and change format
ax = fig.gca()
ax.tick_params(labelsize=12) #tick label font size
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(1.2) #linewith of frame

#linear fiting and plot linear line
m, b = np.polyfit(descriper1, descriper2, 1)
handleFit = plt.plot(descriper1, m*descriper1 + b, linewidth=2, color='red')

#add data tag annotation
for i, name in enumerate(observationName):
    plt.annotate(name, (descriper1[i], descriper2[i]+0.005), fontsize=14, horizontalalignment='center', verticalalignment='bottom')

#add r2 tag
from sklearn.metrics import r2_score
model = np.array([m, b])
predict = np.poly1d(model)
r2 = r2_score(descriper2, predict(descriper1))
r2 = np.round(r2, 2)
#plt.text(0.85, 0.3, 'R2 = {}'.format(r2), fontsize=14)
plt.legend(handles = handleFit, labels = ['$R^2$ = {}'.format(r2)], loc="lower right", handlelength=0, fontsize=14)

plt.show()
fig.savefig(figName2)

############# add metadata into figures ##############
from exif import Image

figNames = ['./'+figName1, './'+figName2]
#>>>dir(Image(figNames[0]))
images = []
for i, image in enumerate(figNames):
    with open(image, "rb") as file:
        images.append(Image(file)) #read figures via exif
print('add metadata: \n', images, '\n')
for i, image in enumerate(images):
    if image.has_exif:
        status = f"contains EXIF (image_description: {image.image_description}) information."
    else:
        status = "does not contain any EXIF information before loading."
    print(f"Image {i} {status}")
    #add metadata to figures
    images[i].image_description = 'file:'+filename+'; sheet:'+sheet  #corresponds to data source
    images[i].Model = 'row_of_tag:'+str(row_of_tag)+'; col_of_tag:'+str(col_of_tag)+'; min_col:'+str(min_col)+'; max_col:'+str(max_col)+'; min_row:'+str(min_row)+'; max_row:'+str(max_row)
    images[i].copyright = "dtu: changai"
    print(f"Description: {images[i].image_description}")
    print(f"Data scope: {images[i].Model}")
    print(f"Copyright: {images[i].copyright} \n")
#rewrite figures    
for i, image in enumerate(figNames):
    with open(image, "wb") as file:
        file.write(images[i].get_file())