# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 10:50:48 2021

@author: babay
"""

# TODO list
#
#   
#   Picking two fittest parents can be used with max(key=fitness_function)
#   
#
# ==============

# Local libraries
import LinReg as lr
import pandas

# Libraries for functioning
import numpy as np
from math import sin, log
import random


# Analytics and plotting
from matplotlib import pyplot as plt
from collections import Counter


# Task e
class SGA():

    # The list of all individuals
    current_population = []

    # Analytics
    mean_fitness = []
    entropy = []
    

    # The default values used are the ones that were found to be performance-wise most promising. 
    
    # Parameters list
    # use_iterations - if True, the GA will stop after it has run itself iteratively "iterations" number of times 
    # threshold - at which threshold the GA should stop if it nos running iteratively
    
    # fitness_function_type - 0 for sin(i), 1 for linreg 
    # maximize - set True if we should be maximizing over the fitness function
    
    # prob-mutation - probability of mutation happening
    
    # print_each_iter - will plot out the population on every iteration
    
    # The rest are pretty self-descriptive
    
    def __init__(self, 
                 
                 # General settings
                 use_iterations = True, 
                 iterations = 10, 
                 use_crowding = False, 
                 threshold = 0.99,
                 
                 # Population parameters
                 population_size = 100, 
                 individual_size = 10, 

                 # Fitness function
                 fitness_function_type = 0,
                 maximize = True,

                 # Mutation
                 mutation = True,
                 prob_mutation = 0.1,
                 
                 # Analytics
                 print_each_iter = False
                 ):
        
        
        # Clear up the current population
        self.clear_current_population()
        
        # Set SGA parameters
        self.iterations = iterations
        self.use_iterations = use_iterations
        self.use_crowding = use_crowding
        self.threshold = threshold
        
        
        # Set the population parameters
        self.population_size = population_size
        self.individual_size = individual_size
        
        # Fitness param
        self.fitness_type = fitness_function_type
        self.maximize = maximize
        
        # Mutation
        self.mutation = mutation
        self.prob_mutation = prob_mutation
        
        # Set the Analytics parameters
        self.print_each_iter = print_each_iter
        
        # Generate initial population
        self.generate_initial_population()
        
        
        # Linreg related
        if (self.fitness_type == 1):
            self.dataset = pandas.read_csv('Dataset.csv', header=None)
            self.linreg = lr.LinReg()
        
        self.run( self.use_iterations, self.iterations, self.use_crowding, self.print_each_iter )
    
    
    # Task e
    
    # Run the algorithm "iterations" times 
    def run(self, use_iterations, iterations, use_crowding, print_each_iter ):
        
        # The actual GA ===========================================================================
        
        # Temp holders
        parents = self.select_parents()       
        offspring = []
        
        # Random parent selection
        # Pick two from the parents mating pool randomly for mating
        for t in range(int(len(parents) * 2 )):
            offspring.extend(self.create_offspring( [random.choice( parents ), random.choice( parents )] ))                                
            
        
        # Apply mutation
        if self.mutation:
            for i in parents:
                if random.random() < self.prob_mutation:                
                    i = self.mutate(i, self.prob_mutation)
                    
            for i in offspring:
                if random.random() < self.prob_mutation:                
                    i = self.mutate(i, self.prob_mutation)
        
        
        # Trims down current_population up to population_size 
        self.select_survivors(parents, offspring, use_crowding)
        
        # Analytics ===========================================================================
        # Accumulate mean fitness data
        self.mean_fitness.append( sum( self.fitness_function(i) for i in self.current_population ) / len(self.current_population))
        
        
        # Entropy 
        
        # Empty list with 
        entropy = [0]* self.individual_size
        
        # Checking number of 1's all individuals for each index
        for individual in self.current_population:
            for index in range(len(entropy)):
                entropy[index] += int( individual[index] )

        # Dividing each by the population size will give the probability of a bit being 1
        for i in range(len(entropy)): 
            entropy[i] = entropy[i] / len(self.current_population)
        
        # Sum the probabilities 
         
        self.entropy.append(0)
        
        # Ignoring the zeros (because log(0) = -inf, but it should be equated to zero, since we multiple by prob 0)
        for e in entropy:
            if e != 0:
                self.entropy[-1] = self.entropy[-1] - e*log(e,2)
        
        
        # Plotting 
        if print_each_iter:
            self.plot()


        # Recursively call to ireate more ===========================================================================       
        if (use_iterations):
            if iterations > 0:
                self.run(use_iterations, iterations-1, use_crowding, print_each_iter  )
        else:
        # Ot if it has not reached the threshold
            if self.maximize:
                if (self.mean_fitness[-1] < self.threshold):
                    self.run(use_iterations, iterations-1, use_crowding, print_each_iter  )
            else:
                if (self.mean_fitness[-1] > self.threshold):
                    self.run(use_iterations, iterations-1, use_crowding, print_each_iter  )
        
    # Task a
    
    # Generates an initial population
    # Individuals are a bitsring with the size individual_size
    def generate_initial_population(self):
        
        # I am so damn proud of this one line below. Returns a randomly generate bitstring
        def generate_individual():
            return ''.join(str(i) for i in [random.randint(0,1) for i in range(self.individual_size) ])
        
        # Generate the entire population
        for i in range(self.population_size):
            self.current_population.append( generate_individual() )

    
    # Taks b
    
    # Will select most fitted individuals from the current_population. The selected pool will be 50% of the current_population size
    def select_parents(self, k = 20):
        
        k = int(self.population_size * k / 100 )
        
        # Picks two fittest individuals from a pool of local_selected 
        def pick_two_fittest( local_selected, fit_selected):
            
            selected = []
            
            # Maximizing fitness
            if self.maximize:
            
                for t in range(2):
                    temp = float('-inf')
                    
                    for i in range(len(fit_selected)):
                        if fit_selected[i] > temp:
                            temp = i
                    
                    # Add the selected individual to the list
                    selected.append(local_selected[i])
                    
                    # Remove the already selected individual
                    del local_selected[i]
                    del fit_selected[i]
            
            # Minimizing fitness
            else:
                for t in range(2):
                    temp = float('inf')
                    
                    for i in range(len(fit_selected)):
                        if fit_selected[i] < temp:
                            temp = i
                    
                    # Add the selected individual to the list
                    selected.append(local_selected[i])
                    
                    # Remove the already selected individual
                    del local_selected[i]
                    del fit_selected[i]
                
            return selected
        
        
        # Keep the track of selected parents
        selected = []


        # Tournament selection based on p.85 Eiben and Smith
        while len(selected) < self.population_size:
            
            # Keeping a small pool of randomly selected individuals
            local_selected = []
                        
            # Select k number of individuals randomly
            for i in range(k):
                local_selected.append( random.choice(self.current_population) )
            
            # Pick two fittest ones
            
            # Decode the individuals
            fit_selected = [ self.decode(i) for i in local_selected ] 
            
            # Select the individuals
            # Manual method for finding the fittest individual
            selected.extend( pick_two_fittest(local_selected, fit_selected)  )

        return selected
        
            
    # Task c
    # Creates offspring - applies recombination to get offpsring from a set of two parents
    def create_offspring(self, selected_parents, recombination = True, rec_type = 0, rec_p = 0.5 ):

        # Generational genetic algorithm
        # The entire population will replaced by the offspring                                
        offspring = []

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
                Exception("Uniform crossover has not been implemented yet.")
            
            else:
                Exception("Unrecognized recombination type in offspring creation.")

        return offspring
    
    
    # Task d
    # use_crowding indicates whether to use (μ, λ) Selection or crowding
    def select_survivors(self, parents, offspring, use_crowding):
        
        # ============================== (μ, λ) Selections
        # p. 89 in Eiben and Smith
        if not use_crowding:
            # The entire pool of survivors are the parents and offspring
            survivors = offspring
            
            # Remove the oldies
            self.clear_current_population()

            # QUESTION Does sorting mess up with probabilities?
            if self.maximize:
                survivors.sort(key= self.fitness_function, reverse = True)
            else:
                survivors.sort(key= self.fitness_function)
            
            
            # Trim down the survivors, keeping only the fittest ones
            self.current_population = survivors[:self.population_size]
            
            
        # ============================== Restricted Tournament Selection
        # P 198 in Simon
        else:
            
            survivors = []
            
            # Picking 20% of the parents for comparison
            k = int(self.population_size * 20 / 100 )
            
            # Each offpsring passes a tournament
            for o in offspring:

                def similarity_coef(i):
                    # Teh coefficient is the difference of real value of the indivduals 
                    return abs(self.decode(i)-self.decode(o))                

                comparison_pool = []
                # Picking k number of random individuals from the parents list
                for i in range(k): comparison_pool.append( random.choice(parents) )
            
                # Find the parent that is most similar to the offspring 
                p = min( comparison_pool, key=similarity_coef)
                
                # And replace if child's fitness is better
                if self.maximize:
                    if self.fitness_function( p ) < self.fitness_function(o):
                        survivors.append(o)
                        parents.remove(p)
                else:
                    if self.fitness_function( p ) > self.fitness_function(o):
                        survivors.append(o)
                        parents.remove(p)
            
            self.current_population = survivors + parents
            
            
    
    # Fitness function that tests the fitness of the bitstring individual
    # fun_type = 0 is for sin(), 1 is for linReg is assigned at the initialization
    def fitness_function(self, individual):
           
        if self.fitness_type == 0:
            return sin( self.decode(individual) )
        
        elif self.fitness_type  == 1:
          return self.linreg.get_fitness(self.dataset, self.linreg.get_columns( self.dataset, individual) )
          
      
    # Simple bit string mutation - returns a mutated individual
    
    # Iterates through the entire individual, and flips a bit with a chance mut_p
    def mutate(self, individual, mut_p):
        for i in range( len(individual)):
            if random.random() < mut_p:            
                individual = individual[:i] + str( int( not int(individual[i]))) + individual[i+1:]
        return individual
                
    
    # Analytics and Plotting        
    # =========================================================
    
    # Plot the sine function
    def plot(self, print_counter = False):
        
        # For plotting the sine function
        sin_x = np.arange(0, 40*np.pi, 0.1)
        sin_y = np.sin(sin_x)
        
        # For plotting the individuals
        ind_x = [ self.decode(i) for i in self.current_population]
        ind_y = [ self.fitness_function(i) for i in self.current_population]
        
        # Plot
        plt.figure()
        
        plt.plot(sin_x, sin_y)
        plt.plot(ind_x, ind_y, 'o')
    
        # Print number of occurences of individuals
        if print_counter: print(Counter(self.current_population) )


    def plot_data(self):
        
        # Mean Fitness
        plt.figure()
        plt.plot( range(len(self.mean_fitness)), self.mean_fitness   )
        plt.xlabel("Generations")
        plt.ylabel("Mean Fitness")
    
    def plot_entropy(self):
        
        # Entropy
        plt.figure()
        plt.plot(range(len(self.entropy)), self.entropy)
        plt.xlabel("Generations")
        plt.ylabel("Entropy")


    # Helpers
    # =========================================================
    
    # Clears up the population array and deletes the individuals
    def clear_current_population(self):
        self.current_population.clear()
        
    # Returns the phenotype of the individual scaled depending on the individual size
    # Expects a bitstring
    def decode(self, individual):
        return int(individual, 2) * 128 / 2**(self.individual_size)

    # Takes a decimal and returns the genotype (e.g. bitstring)
    def encode(self, decimal):
        return format(decimal, "b").zfill(self.individual_size)
    

# ================================================================================================================== End of  class SGA()
    

# Running the code
# Simply use plot(), plot_data(), plot_entropy() after initialization to ge the plots to appear.
# IDE used is Spyder, but should work just fine in others as well


# Running the SGA without crowding, with iterations
sga = SGA(
    # Algorithm specifics
    use_iterations = True, 
    iterations = 30, 
    use_crowding = False,
    
    # Population and Individual params
    population_size = 100, 
    individual_size = 10, 

    # Mutation in offspring
    mutation = True,
    prob_mutation = 0.1,
    
    # Analytics
    print_each_iter = False
    )

sga.plot()
sga.plot_data()
sga.plot_entropy()


# Running the SGA with crowding, letting it stop once the mean average gets close enough to 1 (0.99 in my case)
sga_crowding = SGA(
    
    # Run parameters  
    use_iterations = False,
    use_crowding = True,
    threshold= 0.99,
    
    # Population params
    population_size = 100, 
    individual_size = 8
    
    )

sga_crowding.plot()
sga_crowding.plot_data()
sga_crowding.plot_entropy()


# Running using  without crowding. Will print out the found RMSE (depending on a parameters from one to a few)
sga_linreg = SGA(
    
    # Run parameters    
    use_iterations = True, 
    iterations = 30, 

    # Population parameters    
    population_size = 100,
    individual_size = 10,

    # Fitness function
    fitness_function_type = 1,
    maximize = False
    )


# Print the RMSE values found
for i in Counter( sga_linreg.current_population):
    print( sga_linreg.fitness_function(i) )


# Running using  without crowding. Will print out the found RMSE (usually many)
sga_linreg = SGA(
    
    # Run parameters    
    use_iterations = True,     
    use_crowding = True,
    
    # Population parameters    
    iterations = 200,     
    individual_size = 100,
    
    # Fitness function
    fitness_function_type = 1,
    maximize = False
    )


# Print the RMSE values found
for i in Counter( sga_linreg.current_population):
    print( sga_linreg.fitness_function(i) )