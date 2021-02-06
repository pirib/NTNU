# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:50:48 2021

@author: babay
"""

# Libraries
import numpy as np
from math import sin
import random
import matplotlib.pyplot as plt

# Task e
class SGA():

    # The list of all individuals
    current_population = []
    current_offspring = []

    # The default values used are the ones that were found to be performance-wise most promising
    
    
    # Parameters list
    # population_size   - how many individuals are kept at a given time
    # individual_size   - how many bits are used to represent an individual
    # selection_per     - the percentage of population that is selected on the parent selection step. The rest is discarded.
    
    def __init__(self, population_size = 100, individual_size = 7, selection_per = 50 ):
        
        # Clear up the current population
        self.clear_current_population()
        self.clear_current_offspring()
        
        # Set the population size
        self.population_size = population_size
        self.individual_size = individual_size
        
        # Generate initial population
        self.generate_initial_population()
        
        
    # Task a
    # Generates an initial population
    # Individuals are a bitsring with the size individual_size
    def generate_initial_population(self):
        
        # I am so damn proud of this one line below
        def generate_individual():
            return ''.join(str(i) for i in [random.randint(0,1) for i in range(self.individual_size) ])
        
        # Generate the entire population
        for i in range(self.population_size):
            self.current_population.append( generate_individual() )

    
    # Taks b
    
    # Will select most fitted individuals from the current_population. The selected pool will be 50% of the current_population size
    def select_parents(self, k = 10):
        
        def pick_two_fittest( local_selected, fit_selected):
            
            selected = []
            
            for t in range(2):
                temp = float('-inf')
                
                for i in range(len(fit_selected)):
                    if fit_selected[i] > temp:
                        temp = i
                
                selected.append(local_selected[i])
                del local_selected[i]
                del fit_selected[i]
                
            return selected
        
        # Keep the track of selected parents
        selected = []

        # Tournament selection based on p.85 Eiben and Smith
        while len(selected) < self.population_size/2:
            
            # Keeping a small pool of randomly selected individuals
            local_selected = []
                        
            # Select k number of individuals randomly
            for i in range(k):
                local_selected .append( random.choice(self.current_population) )
            
            # Pick two fittest ones
            
            # Decode the individuals
            fit_selected = [ self.decode(i) for i in local_selected ] 
            
            # Select the individuals
            # Manual method for finding the fittest individual
            selected.extend( pick_two_fittest(local_selected, fit_selected)  )

        return selected
        
            
    # Task c
    # Creates offspring - applies recombination to get offpsring from a set of two parents, then applies mutation
    def create_offspring(self, selected_parents, recombination = True, rec_type = 0, rec_p = 0.5, mutation = True, mut_p = 0.1, mut_bitwise_p = 0.05 ):

        # Generational genetic algorithm
        # The entire population will replaced by the offspring                                
        offspring =[]

        # Apply recombination if valied
        if recombination:
            
            # Get the two parents for easy access
            p1 = selected_parents[0]
            p2 = selected_parents[1]
            
            # One-point crossover
            if rec_type == 0:

                # cp - crossover point 
                # Pick a random point between 0 and len - 1
                cp = random.randint(0, self.individual_size-1)
                
                # Create two kids
                offspring_1 = p1[:cp] + p2[cp:]
                offspring_2 = p2[:cp] + p1[cp:]
                
                # Pack it into the offspring array
                offspring.append(offspring_1)
                offspring.append(offspring_2)
                
            # Uniform crossover
            elif rec_type == 1:
                # TODO me next if there is time
                Exception("Uniform crossovere has not been implemented yet.")
            
            else:
                Exception("Unrecognized recombination type in offspring creation.")

        # Mutate the offspring with a probability mut_p
        if mutation and random.random() < mut_p:
            for o in offspring:         
                o = self.mutate( o, mut_bitwise_p )
                            
        return offspring
    
    
    # Task d
    def select_survivors(self):
        pass
    
    
    # Fitness function that tests the fitness of the bitstring individual
    def fitness_function(self, individual):
        return sin( self.decode(individual) )
                
    
    # Simple bit string mutation - returns a mutated individual
    
    # Iterates through the entire individual, and flips a bit with a chance mut_p
    def mutate(self, individual, mut_p):
        for i in range( len(individual)):
            if random.random() < mut_p:            
                individual = individual[:i] + str( int( not int(individual[i]))) + individual[i+1:]
        return individual
                
    # Analytics and Plotting        
    # =========================================================
    
    # PLot the sine function
    def plot(self):
        
        # For plotting the sine function
        sin_x = np.arange(0, 40*np.pi, 0.1)
        sin_y = np.sin(sin_x)
        
        # For plotting the individuals
        ind_x = [ self.decode(i) for i in self.current_population]
        ind_y = [ self.fitness_function(i) for i in self.current_population]
        
        # Plot
        plt.plot(sin_x, sin_y)
        plt.plot(ind_x, ind_y, 'o')
    
    # Helpers
    # =========================================================
    
    # Clears up the population array and deletes the individuals
    def clear_current_population(self):
        self.current_population.clear()
    
    # Clears up the population array and deletes the individuals
    def clear_current_offspring(self):
        self.current_offspring.clear()
    
    # Returns the phenotype of the individual (e.g integer)
    # Expects a bitstring
    def decode(self, individual):
        return int(individual, 2)

    

# ================================================================================================================== End of  class SGA()
    
    
# Running the SGA
sga = SGA()

sga.plot()
