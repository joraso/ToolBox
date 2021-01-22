# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 19:05:47 2021
A very simple test case for principal component analysis.
@author: Joe Raso
"""

import sys
sys.path.append('../')

from LinearMethods import *

import matplotlib.pyplot as plt

## Creating a sample 2D data set
N = 500; data = np.zeros((N,2))
data[:,0] = np.random.normal(size=N)
data[:,1] = 1*data[:,0] + np.random.normal(size=N)

## Performing PCA
pca = PCA(data)

## Plotting the sample data
plt.scatter(data[:,0],data[:,1])

## Drawing the principal components at the mean
plt.quiver(np.ones((2,1))*pca.xbar[0], # x-component of the mean
           np.ones((2,1))*pca.xbar[1], # y-component of the mean
           pca.V[0,:]*(pca.s), # x and y components of the pca vectors
           pca.V[1,:]*(pca.s), # scaled to the variance
           np.ones((2,1)), angles='xy', scale_units='xy', scale=1)

## A graph of the data set, rotated onto the PC, along with a histogram
## of the distribution on that axis.
#plt.scatter(pca.T[:,0],pca.T[:,1], color='r')
#h, a = pca.distribution(component=0)
#plt.plot(a,h)

## Selecting any number of sample points along the pc, and showing them
## in real space
axis = np.linspace(-4,4)
y = np.zeros((len(axis),2))
for a in range(len(axis)):
    y[a,:] = pca.sample(axis[a], component=0)
plt.scatter(y[:,0],y[:,1], color='r')