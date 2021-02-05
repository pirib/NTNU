# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:50:48 2021

@author: babay
"""

from math import sin
import random


# Task e
class SGA():

    # The list of all individuals
    current_population = []

    # The default values used are the ones that were found to be performance-wise most promising
    
    
    # Parameters list
    # population_size   - how many individuals are kept at a given time
    # individual_size   - how many bits are used to represent an individual
    # selection_per     - the percentage of population that is selected on the parent selection step. The rest is discarded.
    
    def __init__(self, population_size = 1000, individual_size = 6, selection_per = 50 ):
        
        # Clear up the current population
        self.clear_current_population()
        
        # Set the population size
        self.population_size = population_size
        self.individual_size = individual_size
        
        # Generate initial population
        self.generate_initial_population()
        
        
    # Task a
    # Generates an initial population
    # Individuals are a bitsring with the size individual_size
    def generate_initial_population(self):
        
        # I am so proud of this one line below
        def generate_individual():
            return ''.join(str(i) for i in [random.randint(0,1) for i in range(self.individual_size) ])
        
        # Generate the entire population
        for i in range(self.population_size):
            self.current_population.append( generate_individual() )

    
    # Taks b
    def select_parents(self):
        pass
    
            

    # Task c
    # Creates offspring - combines mutation and recombination
    def create_offspring(self, recombination = True, rec_type = 0, rec_p = 0.5, mutation = True, mut_p = 0.1, mut_bitwise_p = 0.05 ):
        
        individual = None
        
        if recombination:
            
            # TODO: Pick two parents
            p1 = None
            p2 = None
            
            # One-point crossover
            if rec_type == 0:
                # cp - crossover point 
                # Pick a random point between 0 and len - 1
                cp = random.randint(0, self.individual_size-1)
                
                offspring_1 = p1[:cp] + p2[cp:]
                offspring_2 = p2[:cp] + p1[cp:]
                
            # Uniform crossover
            elif rec_type == 1:
                # TODO me next!
                pass
            
            else:
                Exception("Unrecognized recombination type in offspring creation.")

        # 
        if mutation:
            self.mutate( individual, mut_bitwise_p )
            
        pass
    
    
    # Task d
    def select_survivors(self):
        pass
    
    
    # Fitness function that tests the fitness of the bitstring individual
    def fitness_function(self, individual):
        return sin( self.decode(individual) )
                
    
    # Simple bit string mutation
    
    # Iterates through the entire individual, and flips a bit with a chance mut_p
    def mutate(self, individual, mut_p):
        for i in range( len(individual)):
            if random.random() < mut_p:            
                individual = individual[:i] + str( int( not int(individual[i]))) + individual[i+1:]
                
    
    # Helpers
    # =========================================================
    
    # Clears up the population array and deletes the individuals
    def clear_current_population(self):
        self.current_population.clear()
    
    # Returns the phenotype of the individual (e.g integer)
    # Expects a bitstring
    def decode(self, individual):
        return int(individual, 2)

    

# ================================================================================================================== End of  class SGA()
    
    
# Running the SGA
sga = SGA()

