# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 21:29:01 2021

@author: changai
"""
import numpy as np
import pandas as pd
import xlrd

# load excel data
def read_excel(filename='./excel_data.xlsx', sheet='Sheet1', min_col=1, max_col=5, min_row=1, max_row=9):  
    row_of_tag = min_row-1 #value 0 means 1st raw in excel;row number of tag
    col_of_tag = min_col-1 #value 0 means 1st(A) coloum in excel; coloum number of tag
    #doc = xlrd.open_workbook(filename).sheet_by_index(sheet)
    doc = xlrd.open_workbook(filename).sheet_by_name(sheet)
    stepsNames = doc.row_values(rowx=row_of_tag, start_colx=min_col, end_colx=max_col) # change 5 into xxx; obtain attributes name
    observationName = doc.col_values(col_of_tag, min_row, max_row) # change 9 into yyy; obtain observation name (0 coloum, 1-8 tags)

    X = np.empty((len(observationName),len(stepsNames)))
    for i in range(len(stepsNames)):
        X[:,i] = np.array(doc.col_values(i+1+col_of_tag ,1+row_of_tag,len(observationName)+1+row_of_tag)).T #raw data 
    return stepsNames, observationName, X


# load csv data
def read_csv(filename = './csv_data.csv', min_col=1, max_col=5):  
    df = pd.read_csv(filename)
    raw_data = df.values
    
    cols = range(min_col, max_col) # change 5 into xxx
    stepsNames = np.asarray(df.columns[cols])  # obtain attributes name
    observationName = raw_data[:, 0] # obtain observation name
    
    X = raw_data[:, cols] # X = np.around(X.astype(np.double), decimals=3) # remain three decimal
    return stepsNames, observationName, X

# load txt data
def read_txt(filename, min_col=1, max_col=5):  #for no blank lines case
    file = open(filename, 'r') 
    stepsNames = file.readline().split()
    
    raw_data = np.loadtxt(filename, usecols=range(min_col-1, max_col), dtype=str, skiprows=1)
    observationName = raw_data[:, min_col-1]
    
    X = raw_data[:, min_col:].astype(float)
    return stepsNames, observationName, X

# read two column txt
def read_two_column_file(filename):  #for no blank lines case
    file = open(filename, 'r') 
    lines = file.readlines()
    x = []
    y = []
    for line in lines:
        p = line.split()
        x.append(float(p[0]))
        y.append(float(p[1]))
    return x, y

# read two column txt with blank lines every x lines; for blank case like PDOS
def read_two_column_PDOS(filename, l, threshold): 
    x = []
    y = []
    file = open(filename, 'r') 
    lines = file.readlines()
    for line in lines[threshold*l+l:threshold*(l+1)+l]:
        p = line.split()
        x.append(float(p[0]))
        y.append(float(p[1]))
    return x, y