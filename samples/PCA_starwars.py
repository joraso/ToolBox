# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 13:18:15 2021
A slightly more complex example of PCA, applied to 538's Star Wars survey.
[America’s Favorite ‘Star Wars’ Movies (And Least Favorite Characters)]
(https://fivethirtyeight.com/features/americas-favorite-star-wars-movies-and-
least-favorite-characters/).
@author: promethustra
"""

import sys
sys.path.append('../')

from PrincipalComponents import *

import matplotlib.pyplot as plt

# Importing the data
data = np.loadtxt('StarWars_cleaned.csv', dtype=str, delimiter=';')

# Strip off top two rows of headers.
# Also srip out respondent ID and geographic region.
headraw = data[:2,1:-1]; data = data[2:,1:-1]

# Parse the header information into a single list
head = []
for i in range(headraw.shape[1]):
    if headraw[1,i] == "Response":
        head.append(headraw[0,i])
    else:
        head.append(headraw[1,i])
    
# Construcing a numerical translation of responses:
numerical = {
# all yes/no questions are scalled -1 to 1
'':0, 'Yes':1, 'No':-1, 
# Have you seen? is converted into a binary
'Star Wars: Episode I  The Phantom Menace':1,
'Star Wars: Episode II  Attack of the Clones':1,
'Star Wars: Episode III  Revenge of the Sith':1,
'Star Wars: Episode IV  A New Hope':1,
'Star Wars: Episode V The Empire Strikes Back':1,
'Star Wars: Episode VI Return of the Jedi':1,
'1':1, '2':2, '3':3, '4':4, '5':5, '6':6,
# character favorability is on a percentage rating -100 - 100
'Very favorably':100,
'Somewhat favorably':50,
'Unfamiliar (N/A)':0,
'Neither favorably nor unfavorably (neutral)':0,
'Somewhat unfavorably':-50,
'Very unfavorably':-100,
# Who shot first?
'Greedo':-1, 'Han':1,
"I don't understand this question":0,
# respondent gender is from -1 (female) to 1 (male)
'Male':1, 'Female':-1,
# Age, income and education are converted into a scale
'18-29':1, '30-44':2, '45-60':3, '> 60':4,
'$0 - $24,999':1,'$25,000 - $49,999':2,'$50,000 - $99,999':3,
'$100,000 - $149,999':4, '$150,000+':5,
'Less than high school degree':1,
'High school degree':2,
'Some college or Associate degree':3,
'Bachelor degree':4, 'Graduate degree':5}
# Implementing the numerical interpretation of the data
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        data[i,j] = numerical[data[i,j]]
# Correct the data type
data = np.array(data, dtype=float)

# Finally, PCA:
pca = PCA(data)

# Printing a graph of the fraction of variance explained
#plt.plot(pca.s/np.sum(pca.s))
# 0th component is by far the most significant, with 1st about half the weight.
# Components 2-13 are somwhat significant, components 14+ are noise.

# I'm curious to see the distribution of the first 2 components
#plt.scatter(pca.T[:,0],pca.T[:,1])

# Looking at the distribution on component 0:
#h, a = pca.distribution(component=1)
#plt.plot(a,h)

# Function for textual interpreting numerical sample
def interpret(x):
    for i in range(len(head)):
        print("{}: {}".format(head[i],x[i]))
        
# Who is the mean respondent?
interpret(pca.xbar)        
        
# Who is this average fan outside the mean in the first 2 components
#x = pca.sample([10.3, 85.4])
#interpret(x)