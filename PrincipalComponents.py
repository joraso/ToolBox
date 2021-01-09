# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:56:53 2021
Principal Component Analysis Tools
@author: Joe Raso
"""

import numpy as np

class PCA:
    """Object representing the principal component analysis of input X.
    Parameters:
        X - (ndarray) The data matrix, with rows as samples, and columns as
            dimensions. (Is not required to be mean-zero.)
    Attributes:
        X - (ndarray) The original input data.
        xbar - (ndarray) the mean sample (row) of X.
        B - (ndarray) The data X, shifted to mean-zero.
        C - (ndarray) The covariance matrix of B, normalized to the number of
            samples.
        s - (ndarray) Variance along each principal component, sorted by
            magnitude, normalized to the number of samples (rows of X).            
        V - (ndarray) Loadings of each principal component as column vectors,
            sorted by magnitude of the variance (same order as v), oriented
            to put the first dimension of the first principal component in
            the positive
            direction.
        T - (ndarray) The data X, rotated into the PCA basis."""
    def __init__(self, X):    
        # Bringing the data to mean-zero
        xbar = np.average(X,axis=0)
        B = X - np.ones(X.shape)*xbar
        # Compute the correlation matrix
        C = np.dot(B.transpose(),B) / X.shape[0]
        # Eigenvector analysis
        u, v = np.linalg.eig(C)
        # Sorting in order of decending variance
        a = np.argsort(u)
        s = np.zeros(u.shape); V = np.zeros(v.shape)
        for i in range(len(a)):
            s[-1-i] = u[a[i]]
            V[-1-i] = v[:,a[i]]
        V = V*np.sign(V[0,0])
        # Generating rotated data
        T = np.dot(X,V)
        # Storing results:
        self.X = X
        self.xbar = xbar
        self.B = B
        self.C = C
        self.s = s
        self.V = V
        self.T = T