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