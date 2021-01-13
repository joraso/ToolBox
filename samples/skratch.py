# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:30:55 2021
Sktatch space
@author: promethustra
"""

# Compile a list text of responses present in each column
responses = []
for i in range(data.shape[1]):
    options = set(data[:,i])
    responses.append(list(options))