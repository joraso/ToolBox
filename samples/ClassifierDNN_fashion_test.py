# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:33:07 2021
A simple example/test using the MNST fashion data set.
https://github.com/zalandoresearch/fashion-mnist
@author: Joe Raso
"""

import sys
sys.path.append('../')

from NeuralNets import *
import matplotlib.pyplot as plt

# Load up the fashion data set
(xtrain, ytrain), (xtest, ytest) = tf.keras.datasets.fashion_mnist.load_data()

label_key = {0:"T-Shirt/Top",1:"Trouser",2:"Pullover",
             3:"Dress",4:"Coat",5:"Sandal",6:"Shirt",
             7:"Sneaker",8:"Bag",9:"Ankle boot"}

# make and train
net = CatagoryNet((28,28), 10, [784, 196, 196, 49])
net.train(xtrain, ytrain, batch=5000, epochs=20)

# if you wanna see the accuracy or loss
plt.plot(net.accuracy)
plt.plot(net.loss)

def RandTest():
    """quick little function to test the model with some random samples."""
    # Pick som random images from the test set.
    ims = np.random.randint(0, len(ytest), size=4)
    guesses = net.predict(xtest[ims,:,:])
    # Now to draw it
    fig, axes = plt.subplots(2, 2)
    axs = [axes[0][0],axes[0][1],axes[1][0],axes[1][1]] # have to reindex them
    for j in range(4):
        axs[j].imshow(xtest[ims[j],:,:], cmap='Greys', interpolation='none')
        axs[j].text(0,1.5,"Guessing {}".format(label_key[guesses[j]]))
        axs[j].text(0,3.5,"Actually a {}".format(label_key[ytest[ims[j]]]))
        
# An interesting idea...
yguess = net.predict(xtest)
bubbles = np.zeros((10,10))
for i in range(len(ytest)):
    bubbles[yguess[i],ytest[i]] += 1
x = np.linspace(0,9,num=10); y = np.linspace(0,9,num=10)
x, y = np.meshgrid(x, y)
plt.scatter(x.reshape(100),y.reshape(100),s=950*bubbles.reshape(100),alpha=0.5)
plt.xlabel("Actual Catagory")
plt.ylabel("Network Guess")