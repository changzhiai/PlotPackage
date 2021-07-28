# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 17:07:38 2021

@author: changai
"""

import json
import numpy as np
  
  
# the file to be converted to 
# json format
filename = '../data/data.txt'
  
# dictionary where the lines from
# text will be stored
dict1 = {}

# creating dictionary
with open(filename) as fh:
  
    for line in fh:
  
        # reads each line and trims of extra the spaces 
        # and gives only the valid words
        command, description = line.strip().split(None, 1)
  
        dict1[command] = float(description.strip())
  
# creating json file
out_file = open("../data/output.json", "w")
json.dump(dict1, out_file, indent = 4, sort_keys = False)
out_file.close()

f = open('../data/output.json', 'r') # open file in read mode
data = f.read()      # copy to a string
f.close()               # close the file
print(data)          # print the data