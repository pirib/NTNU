# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:34:05 2021

@author: babay
"""

import tensorflow as tf
import numpy as np
import splitgd



class NN(splitgd.SplitGD):
    
    
    # Initialize the object
    def __init__(self, layers):
        self.generate_network(layers)
        super().__init__(self.model)


    # The grid object is used the number of input neurons
    # layers - a tuple with number of neurons per hidden layer (the input and output are handled automatically)
    def generate_network(self, layers, 
                         optimizer = 'adam',
                         loss = 'mean_squared_error'
                         ):
    
        # Create the model
        self.model = tf.keras.models.Sequential()

        # Adding the input layer
        self.model.add(tf.keras.layers.InputLayer(input_shape = (int(layers[0]),) ) )

        # Adding layers with number of nodes as specified in layers argument
        for num_nodes in layers[1:]:
            self.model.add( tf.keras.layers.Dense( units = num_nodes , activation = tf.nn.relu))
    
        # The output neuron returns the V(s)
        self.model.add( tf.keras.layers.Dense( units = 1 , activation = tf.nn.relu))
        
        # Compile the model
        self.model.compile(optimizer = optimizer, loss = loss)
        

        
    def fit(self, x, y, l_rate):
        
        # Set the dimensions of the training data
        st = np.array(x)        
        st = st.astype(np.float)
        st = np.expand_dims(st, 0)
        
        # Conver to np array
        td = np.expand_dims(y, 0)
        
        super().fit(st, td, l_rate, verbosity=0)



    
    
    