"""
Created on Wed May 22 12:40 2024
Example of how to construct a basic model in pytorch.
@author: Joe Raso
"""

import numpy as np
import pandas as pd
import torch as pt

class SimpleTorchNN(pt.nn.Module):
    # Torch model are subclassed from pt.nn.Module
    def __init__(self):

        # Must init the parent before anything else
        super(SimpleTorchNN, self).__init__()

        #Define the layers ('Linear' is the basic dense layer)
        self.layer1 = pt.nn.Linear(
            13, # input features
            9, # output features
            bias=True) # learn an additive bias
        self.layer2 = pt.nn.Linear(9, 5, bias=True)
        self.layer3 = pt.nn.Linear(5, 2, bias=False)

        # Manually define the loss function
        # This will be required to take the gradient of the parameters
        self.loss_fn = pt.nn.MSELoss(reduction='mean')

        # Manually define the optimizer.
        # To do this we must provide an iterable of parameters that will be
        # updated. e.g.

        # params = [p for p in net.layer1.parameters()]

        # Conveniently calling the pt.nn.Module init provides a method
        # .parameters() that produces a generator function for Module
        # parameters; It seems to auto-detect any torch layer-type objects
        # bound to the class.
        self.optimizer = pt.optim.Adam(
            self.parameters(), lr=0.001)


    def forward(self, X):
        # Torch models must define a "forward" method for graph contruction
        # This simply passes the data through the layers, using their
        # __call__() methods:
        X = self.layer1(X)
        X = self.layer2(X)
        X = self.layer3(X)
        return X

    def batch_train(self, X, y):

        # forward() can only take a tensor, so we have to do some typing
        if type(X) == pd.DataFrame:
            X = X.to_numpy()
        if type(X) == np.ndarray:
            X = pt.Tensor(X)

        # Obtain the y prediction
        y_pred = self.forward(X)

        # Calculate the loss
        loss = self.loss_fn(y_pred, y)

        # Backpropigate the tensor graph
        loss.backward()

        # Step the optimizer
        self.optimizer.step()

        # Lets print the loss, for posterity
        print(f"Loss: {loss.item():.2f}")
