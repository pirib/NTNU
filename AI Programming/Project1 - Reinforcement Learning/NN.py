# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:34:05 2021

@author: babay
"""

import tensorflow as tf

import splitgd



class NN():

    model = None    

    # Initializa the object
    def __init__(self, layers):
        self.generate_network(layers)


    # The grid object is used the number of input neurons
    # layers - a tuple with number of neurons per hidden layer (the input and output are handled automatically)
    def generate_network(self, layers, 
                         optimizer = 'SGD',
                         loss = 'mean_squared_error'
                         ):
    
        # Create the model
        self.model = tf.keras.models.Sequential()

        # Adding layers with numbed of nodes as specified in layers argument
        for num_nodes in layers: 
            self.model.add( tf.keras.layers.Dense( num_nodes , activation = tf.nn.relu )  )
    
        # The output neuron returns the V(s)
        self.model.add( tf.keras.layers.Dense( 1, activation = tf.nn.relu )  )
        
        # Compile the model
        self.model.compile(optimizer = optimizer, loss = loss)
    
        
    def fit(self, x, y):
        
        self.model.fit( x , y , epochs = 100)
        
        # TODO - we need to call splitgd.fit here instead to hijack the gradient computation
        

    # TODO model.summary()
    
    
    
    
    
    
    
    
    
    
    
    
    