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
data[:,1] = 3*data[:,0] + np.random.normal(size=N)
plt.scatter(data[:,0],data[:,1])
s, V = principal_components(data)
# Drawing the principal component at the origin
plt.quiver(np.zeros((2,1)),np.zeros((2,1)),
            V[0,:],V[1,:], np.ones((2,1)),
            angles='xy', scale_units='xy', scale=1)