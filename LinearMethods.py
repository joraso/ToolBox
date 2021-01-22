# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:56:53 2021
Linear Algebra Analysis Tools
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
    def distribution(self, component=0, nbins=50, binmin=None, binmax=None):
        """Returns a flattened histogram of data along the specified principal
        component (defaults to the first)."""
        # Handling default bounds
        if binmin == None:
            binmin = np.min(self.T[:,component])
        if binmax == None:
            binmax = np.max(self.T[:,component])
        # Returning the distribution
        [h, edges] = np.histogram(self.T[:,component],bins=nbins,
                            range=(binmin, binmax))
        axis = (edges[1:]-edges[:-1])/2 + edges[:-1]
        return h, axis
    def sample(self, x):
        """returns a representative sample from the value x of the principal
        components.
        Parameters:
        x - (float or list) The vector of principal components to be
            interpreted. If an int, it's assumed the first component, if a
            list, it's assumed to be a list of the first several components
            in order. (components other than those listed are set to zero)."""
        t = np.zeros(self.xbar.shape)
        if type(x) == float:
            t[0] = x
        elif type(x) == list:
            for i in range(len(x)):
                t[i] = x[i]
        return self.xbar + np.dot(t, np.linalg.inv(self.V))