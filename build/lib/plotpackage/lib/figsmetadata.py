# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 11:43:32 2021

@author: changai
"""

from exif import Image

#for identifying pictures
class FigsMetaData:
    def __init__(self, fignames, filename, sheet, min_col, max_col, min_row, max_row):
        self.figNames = fignames
        self.filename = filename
        self.sheet = sheet
        self.min_col = min_col
        self.max_col = max_col
        self.min_row = min_row
        self.max_row = max_row
        
    def add_metadata(self):        
        #>>>dir(Image(figNames[0]))
        row_of_tag = self.min_row-1 #value 0 means 1st raw in excel;row number of tag
        col_of_tag = self.min_col-1 #value 0 means 1st(A) coloum in excel; coloum number of tag
        images = []
        for i, image in enumerate(self.figNames):
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
            images[i].image_description = 'file:'+self.filename+'; sheet:'+self.sheet  #corresponds to data source
            images[i].Model = 'row_of_tag:'+str(row_of_tag)+'; col_of_tag:'+str(col_of_tag)+'; min_col:'+str(self.min_col)+'; max_col:'+str(self.max_col)+'; min_row:'+str(self.min_row)+'; max_row:'+str(self.max_row)
            images[i].copyright = "dtu: changai"
            print(f"Description: {images[i].image_description}")
            print(f"Data scope: {images[i].Model}")
            print(f"Copyright: {images[i].copyright} \n")
        #rewrite figures
        for i, image in enumerate(self.figNames):
            with open(image, "wb") as file:
                file.write(images[i].get_file())