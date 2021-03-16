"""
Created on Mon Mar 15 11:04:55 2021

@author: babay
"""
import pandas as pd

import random
from math import log

# The decision Tree algorithm, basically code of the pseudo-code from the book
def decisionTreeLearning(examples, attributes, parent_examples):
    
    if not examples:
        return pluralityValue(parent_examples)

    elif examples.nunique() == 1:
        return { "None" : bool(examples[0]) }
    elif not attributes:
        return pluralityValue(examples)
    
    else:
        A = argmax( attributes, examples, importance )
        
        tree = A
        
        for a in A:
            exs = None
            subtree = decisionTreeLearning(exs, attributes.remove(A), examples)
            # Stuff here        
            tree.append(subtree)

    return tree

# Plurality Value from the book
def pluralityValue(examples):
    
    # Lazy way of doing it, but i know it is just two possiblities
    n_true = examples["Survived"].value_counts()[1]
    n_false = examples["Survived"].value_counts()[0] 
    
    if n_true == n_false: 
        return bool(random.randint(0, 1))
    elif n_true > n_false: 
        return True
    else: 
        return False

# Importance function, that returns the gain based on the attribute in the examples set
def importance(a, examples):
    
    # Using Tom Mitchell's books notation for entropy, because the book in syllabus is absolute garbage
    # Total number of positives and negatives 
    p = examples["Survived"].value_counts()[1]
    n = examples["Survived"].value_counts()[0]
    
    # Calculating the entropy and remainder separately
    def B(p, n):
        q = p / ( p + n )
        
        a = 0
        b = 0
        
        # Need to make sure that 0 log(0) is actually 0
        if q != 0:
            a = q*log(q,2)
        
        if 1-q != 0:
            b = (1-q)*log(1-q,2)
        
        return -(a + b)
    
    # Calculates the remainder
    def remainder(a):
        
        remainder = 0
        
        for v in examples[a].unique():
            
            pk = examples.loc[ (train_df[a] == v) & (train_df["Survived"] == 1) ]
            nk = examples.loc[ (train_df[a] == v) & (train_df["Survived"] == 1) ]
            
            remainder += (pk + nk)/ ( p + n ) * B (pk, nk)
            
        return remainder
        
    # Could have just returned the - remainder, and the did arcmin instead of arcmax, but whatever. Manually calculate B(Goal) it is always the same.
    return B( p, n ) - remainder(a)

# Helper functions

# Argmax, nothing much to say here
def argmax(attributes, examples, importance):
    
    # Temo values for comparison
    gain = 0
    attribute_name = ""
    
    for a in attributes:
        if importance(a) > gain:
            gain = importance(a)
            attribute_name = a
    
    return attribute_name



# Getting the data into dataframes
train = pd.read_csv("./data/train.csv")
test = pd.read_csv("./data/test.csv")


# Ignoring the Name, TicketNumber, Passenger Fare, Cabin numbers, Embarked
# These are very unlikely to influence the Survival rate - a more comprehesive explanation can be found in the pdf.

# Get the attributes and then remove the unnecessary ones
attributes = train.keys().tolist()
[attributes.remove(a) for a in ['Name', 'Fare', 'Ticket', 'Cabin', 'Embarked']]

print( train )



# Running the code