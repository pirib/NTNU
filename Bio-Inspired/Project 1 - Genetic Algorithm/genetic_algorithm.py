# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:50:48 2021

@author: babay
"""

from math import sin
import random


# Bitstring individual
class individual():
        
    def __init__(self, bitstring_size = 6):
        self.size = bitstring_size
        self.value = self.generate()    
    
    # I am so damn proud of this line
    # Generates and returns a bitstring of size bitstring_size
    def generate(self):
        return ''.join(str(i) for i in [random.randint(0,1) for i in range(self.size) ])


    def encode(self):
        pass
    
    # Returns the phenotype of the individual (e.g integer)
    def decode(self):
        return int(self.value, 2)
    
    

# Task e
class SGA():

    # The default values used are the ones that were found to be performance-wise most promising
    def __init__(self, population_size = 1000 ):
        self.population_size = population_size
        
        

    # Task a
    def generate_initial_population(self):
        pass
    
    
    # Taks b
    def select_parents(self):
        pass
    
    
    # Task c
    # Creates offspring - combines mutation and recombination
    def create_offspring(self, recombination = True, rec_type = 0, rec_p = 0.5, mutation = True, mut_type = 0, mut_p = 0.1 ):
        
        if mutation:
            pass
        
        if recombination:
            pass
            
        pass
    
    
    # Task d
    def select_survivors(self):
        pass
    
    
    
    
# Running the SGA
sga = SGA()

