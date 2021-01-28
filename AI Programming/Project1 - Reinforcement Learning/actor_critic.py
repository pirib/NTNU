# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 18:52:41 2021

@author: babay
"""
import grid

class Critic():
    
    # Mode: 0 for tabular, 1 for neural network
    # 
    def __init__(self, mode = 0, learning_step = 0.01, elig_rate = 0.5, discount = 0.09):
        self.mode = mode
        self.learning_step = learning_step
        self.elig_rate = elig_rate
        self.discoun = discount
        
        
        
        
        
class Actor():
    
    def __init__(self, learning_step = 0.01, greed_rate = 0.1 , elig_rate = 0.5, discount = 0.09):
        self.learning_step = learning_step
        self.greed_rate = greed_rate
        self.elig_rate = elig_rate
        self.discount = discount
        
        
    
