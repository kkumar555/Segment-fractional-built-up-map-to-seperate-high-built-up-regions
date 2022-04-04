# -*- coding: utf-8 -*-
"""
create_segments_of_high_built_region.py

Krishna Kumar Perikamana
04.04.2022 
https://www.researchgate.net/profile/Krishna-Kumar-Perikamana

Try to divide high built-up region into multiple segments based on the neighbourhood level
characteristic.

"""

import numpy as np
import math
import random
from pyrsgis import raster
import matplotlib.pyplot as plt
import skimage.segmentation as seg
import skimage.color as color
from scipy.stats import mode
import cv2

#load the raster
ds,R1 = raster.read(r'''.\input\190205_Bangalore_Landsat8_ra_30m_utm43n_Fractional_Built.tif''')
print("Raster cell size is", R1.shape)

nr = R1.shape[0]
nc = R1.shape[1]

#select only high built region
A1 = np.zeros((nr,nc))
for i in range(0,nr):
    for j in range(0,nc):
        if(R1[i,j]>80 and R1[i,j]<=100):
            A1[i,j]=R1[i,j]

#cluster image points
image_slic = seg.slic(A1,n_segments=150,compactness=0.8,sigma=8,max_size_factor=25.0)

#find unique values and create image
uq = np.unique(image_slic)
im = np.zeros((nr,nc))
for k in range(0,np.unique(image_slic).size):
    for i in range(0,image_slic.shape[0]):
        for j in range(0,image_slic.shape[1]):
            if(image_slic[i,j]==uq[k]):
                im[i,j] = k+1
     
#get the intersection region
ima = np.zeros((nr,nc))
for i in range(0,nr):
        for j in range(0,nc):
            if(A1[i,j]!=0):
                ima[i,j] = im[i,j]
    
#Saving the image 
raster.export(ima, ds, '190205_Bangalore_Landsat8_ra_30m_utm43n_Fractional_Built_segments2.tif', dtype='float')

