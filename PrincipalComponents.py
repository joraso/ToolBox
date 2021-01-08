# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:56:53 2021
Principal Component Analysis Tools
@author: Joe Raso
"""

import numpy as np

def principal_components(X):
    """Performs the basic function of principal component analysis.
    Input:
        X - (ndarray); the data matrix, with rows as samples, and columns as
            dimensions. (Is not required to be mean-zero.)
    Output:
        s - (ndarray); variance along each principal component, sorted by
            magnitude.            
        V - (ndarray); loadings of each principal component as column vectors,
            sorted by magnitude of the variance (same order as v)"""
    # Bringing the data to mean-zero
    Xbar = np.ones(X.shape)*np.average(X,axis=0)
    B = X - Xbar
    # Compute the correlation matrix
    C = np.dot(B.transpose(),B)
    # Eigenvector analysis
    u, v = np.linalg.eig(C)
    # Sorting in order of decending variance
    a = np.argsort(u)
    s = np.zeros(u.shape); V = np.zeros(v.shape)
    for i in range(len(a)):
        s[-1-i] = u[a[i]]
        V[-1-i] = v[:,a[i]]
    return s, V