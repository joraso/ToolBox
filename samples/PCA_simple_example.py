# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 19:05:47 2021
A very simple test case for principal component analysis.
@author: Joe Raso
"""

import sys
sys.path.append('../')

from PrincipalComponents import *

import matplotlib.pyplot as plt

# Creating a sample 2D data set
N = 500; data = np.zeros((N,2))
data[:,0] = np.random.normal(size=N)
data[:,1] = 1*data[:,0] + np.random.normal(size=N)

plt.scatter(data[:,0],data[:,1])

pca = PCA(data)

# Drawing the principal components at the mean
plt.quiver(np.ones((2,1))*pca.xbar[0], # x-component of the mean
           np.ones((2,1))*pca.xbar[1], # y-component of the mean
           pca.V[0,:]*(pca.s), # x and y components of the pca vectors
           pca.V[1,:]*(pca.s), # scaled to the variance
           np.ones((2,1)), angles='xy', scale_units='xy', scale=1)
            
#plt.scatter(pca.T[:,0],pca.T[:,1], color='r')