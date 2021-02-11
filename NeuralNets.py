# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 13:32:32 2021
@author: Joe Raso
"""

import numpy as np
import tensorflow as tf

class ClassifierNet:
    """ A neural network design to solve classification problems such as
        image recognition. The basic construction is an input layer, followed
        by any number of interstitial dense layers (specified by 'structure'),
        and an output layer. The output is a normalized vector of size
        ncatagories, which contains something equivalent to the estimated
        likelyhood that the input sample belongs in that catagory.
        
        Arguments:
        inputdims   - (tuple) Dimensions of the input data.
        ncatagories - (int) Number of catagories.
        structure   - (list) List of ints specifying the dimensionality (number
                      of neurons) of the interstitial layers.
                      
        
        params      - (dict) Other parameters. A dictionary of values to set
                      the attributes (if different from their default values).
        
        Attributes:
        inputdims   - (tuple) Dimensions of the input data.
        ncatagories - (int) Number of catagories.
        structure   - (list) List of ints specifying the dimensionality of the
                      interstitial layers.
        activation  - (str) Keras activation function to be used in the inter-
                     stitial layers. defaults to 'relu'.
        optimizer   - (str) Keras optimizer to use during training. defaults
                     to 'adam'.
        verbose     - (bool) Toggles command line output. Defaults to 1 (T)."""
    def __init__(self, inputdims, ncatagories, structure, params={}):
        
        self.inputdims = inputdims
        self.ncatagories = ncatagories
        self.structure = structure
        default_params = {'activation':'relu', 'optimizer':'adam', 'verbose':1}    
        self.__dict__.update(default_params)
        self.__dict__.update(params)
        # Attributes not created by the user
        self.layers = []
        self.model = None
        # History tracking
        self.loss=[]; self.accuracy=[]
        # Now build it.
        self.build()
        
    def build(self):
        """Constructs the model from the specified structure."""
        # Input layer
        self.layers = [tf.keras.layers.Flatten(input_shape=self.inputdims)]
        # Interstitial layers
        for i in self.structure:
            self.layers.append(tf.keras.layers.Dense(i,
                               activation = self.activation))
        # output layer
        self.layers.append(tf.keras.layers.Dense(self.ncatagories,
                                activation='softmax'))
        # compiling
        self.model = tf.keras.Sequential(self.layers)
        self.model.compile(optimizer=self.optimizer, metrics=['accuracy'],
                           loss='sparse_categorical_crossentropy')
                           
    def train(self, xtrain, ytrain, batch=1, epochs=1):
        """Trains the model on the given data set.
        Arguments:
        xtrain - (ndarray) Input training data.
        ytrain - (ndarray) Training labels, expected to be an array of ints in
                 the range [0, ncatagories).
        Keywords:
        batch  - (int) Batch size. defaults to 1.
        epochs - (int) Number of epochs. defaults to 1.
        """
        self.model.fit(xtrain, ytrain, batch_size=batch, epochs=epochs,
                       verbose=self.verbose, shuffle=True)
        self.loss += (self.model.history.history['loss'])
        self.accuracy += (self.model.history.history['acc'])
        
    def predict(self, xset):
        """Returns the catagory predictions on a test data set. Uses the simple
        most likely catagory given the vector output of the model.
        Arguments:
        xset - (ndarray) The set of input data to catagorize. Note that the
               function expects a batch of samples to predict, so take care
               when predicting a singular data sample that the dimensions are
               consistent with a batch containing many samples (i.e. it should
               have a 0-axis corrosponding to the sample number).
        """
        pred = self.model.predict(xset)
        return np.argmax(pred, axis=1)
        
        
class AutoEncoder():
    """ The simplest possible auto-encoder neural network design. The basic 
        construction is:
        
            input -> encoder -> latent -> decoder -> output
        
        The encoder consists of an input layer, followed by any number of
        interstitial dense hidden layers (specified by 'structure'), then a low
        dimensional latent layer. The decoder archetecture is mirror to the
        encoder. The loss function is the binary cross-entropy between the
        intou and the reconstructed output.
        
        Arguments:
        inputdims   - (int) Dimensions of the input data. Note that this
                      network does not perform any data reshaping.
        latentdims  - (int) Dimension of the latent space.
        structure   - (list) List of ints specifying the dimensionality (number
                      of neurons) of the interstitial hidden layers.
        params      - (dict) Other parameters. A dictionary of values to set
                      the attributes (if different from their default values).
        
        Attributes:
        inputdims   - (tuple) Dimensions of the input data.
        latentdims  - (int) Dimension of the latent space.
        structure   - (list) List of ints specifying the dimensionality of the
                      interstitial hidden layers.
        activation  - (str) Keras activation function to be used in the inter-
                     stitial layers. defaults to 'relu'.
        optimizer   - (str) Keras optimizer to use during training. defaults
                     to 'adam'.
        verbose     - (bool) Toggles command line output. Defaults to 1 (T)."""
    def __init__(self, inputdims, latentdims, structure, params={}):
        # Note: input does not perform reshaping
        self.inputdims = inputdims
        self.latentdims = latentdims
        self.structure = structure
        default_params = {'activation':'relu', 'optimizer':'adam', 'verbose':1}    
        self.__dict__.update(default_params)
        self.__dict__.update(params)
        # History tracking
        self.loss=[]; self.accuracy=[]
        # Do the thing:
        self.Build()
    def Build(self):
        """Constructs the model from the specified structure."""
        def connect(input_layer, layers):
            # Connects a given list of layers and returns output layer
            layer = input_layer
            for l in layers:
                layer = l(layer)
            return layer
        # Define the encoder layers:
        self.input = tf.keras.Input(shape=self.inputdims) 
        self.encoding_layers = []
        for i in self.structure:
            self.encoding_layers.append(tf.keras.layers.Dense(i,
                    activation=self.activation))
        self.latent = tf.keras.layers.Dense(self.latentdims,
                activation = self.activation)
        self.encoding_layers.append(self.latent)
        # Define the decoding layers:
        self.encoded_input = tf.keras.Input(shape=self.latentdims) 
        self.decoding_layers = [tf.keras.layers.Dense(self.structure[-1],
                activation = 'sigmoid')]
        for i in reversed(self.structure[:-1]):
            self.decoding_layers.append(tf.keras.layers.Dense(i,
                    activation=self.activation))
        self.output = tf.keras.layers.Dense(self.inputdims,                                            
                activation = self.activation)
        self.decoding_layers.append(self.output)
        # Build the intertwinned models
        self.encoder = tf.keras.Model(self.input,
                connect(self.input, self.encoding_layers))
        self.decoder = tf.keras.Model(self.encoded_input,
                connect(self.encoded_input, self.decoding_layers))
        self.autoencoder = tf.keras.Model(self.input,
                connect(self.input, self.encoding_layers+self.decoding_layers))
        # Compile the auto encoder for training (the intertwined models do
        # not need compiling, since we don't train them individually)
        self.autoencoder.compile(optimizer=self.optimizer,
                metrics=['accuracy'], loss='binary_crossentropy')
                
    def train(self, xtrain, batch=1, epochs=1):
        """Trains the model on the given data set.
        Arguments:
        xtrain - (ndarray) Input training data.
        Keywords:
        batch  - (int) Batch size. defaults to 1.
        epochs - (int) Number of epochs. defaults to 1.
        """
        self.autoencoder.fit(xtrain, xtrain, batch_size=batch, epochs=epochs,
                       verbose=self.verbose, shuffle=True)
        self.loss += (self.autoencoder.history.history['loss'])
        self.accuracy += (self.autoencoder.history.history['acc'])
    
    def Encode(self, xdata):
        """Returns the latent space/encoded representation of the data.
        Arguments:
        xdata - (ndarray) Input data.
        Returns:
        xdata - (ndarray) Encoded representation of the data."""
        return self.encoder.predict(xdata)
    def Decode(self, zdata):
        """Returns the reconstruction of output data based on space/encoded
        representation.
        Arguments:
        zdata - (ndarray) Input encoded data.
        Returns:
        xdata - (ndarray) Decoded/reconstructed output data."""
        return self.decoder.predict(zdata)