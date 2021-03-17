"""
Created on Mon Mar 15 11:04:55 2021

@author: babay
"""


import pandas as pd
import copy
import random
from math import log

# A class of tree, adopted from older code of mine
class Tree():
    
    def __init__(self, label):
        self.label = label
        self.branches = []


# The decision Tree algorithm, basically python code of the pseudo-code from the book
def decisionTreeLearning(examples, attributes, parent_examples):

    if examples.empty:
        return pluralityValue(parent_examples)
    
    elif examples["Survived"].nunique() == 1:
        return examples["Survived"].unique()[0]       
    
    elif not attributes:
        return pluralityValue(examples)
    
    else:

        A = argmax( attributes, examples, importance )
        
        tree = Tree(A)

        for vk in examples[A].unique():
            
            exs = examples.loc[ (examples[A] == vk) ]

            new_attributes = copy.deepcopy(attributes)
            new_attributes.remove(A)  

            subtree = decisionTreeLearning(exs, new_attributes , examples)
            
            tree.branches.append( [vk, subtree] )
            
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
        
        if (p + n == 0):
            return 0
        
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
            pk = len(examples.loc[ (train[a] == v) & (examples["Survived"] == 1) ].index)
            nk = len(examples.loc[ (train[a] == v) & (examples["Survived"] == 1) ].index)

            remainder += (pk + nk)/ ( p + n ) * B (pk, nk)
            
        return remainder
        
    # Could have just returned the - remainder, and the did arcmin instead of arcmax, but whatever. Manually calculate B(Goal) it is always the same.
    return B( p, n ) - remainder(a)

# Argmax, nothing much to say here
def argmax(attributes, examples, importance):
    
    # Temp values for comparison
    gain = 0
    attribute_name = None
    
    for a in attributes:
        imp = importance(a, examples)
        if imp >= gain:
            gain = imp
            attribute_name = a
    
    if attribute_name == None:
        attribute_name = random.choice(attributes)
    
    return attribute_name

# A depth-first search in the tree, expects a row from a dataframe, returns the value of the leaf node.
def test_tree(tree):
    
    # Does the actual looping
    def int_test(row):
        
        root = tree
        # Looping until we in a nutshell find the leaf node we are after
        
        while(True):
    
            hit = False
            
            # Loop through the branches
            for branch in root.branches:
                
                # Found it
                if branch[0]==row[root.label]:
                    
                    hit = True
    
                    if isinstance(branch[1], Tree): 
                        root = branch[1]
    
                    else: 
                        return branch[1]
                    
            # If did not find, carry on with the depth first search
            if not hit:
                
                branch = root.branches[ random.randint(0, len(root.branches)-1) ]
    
                if isinstance(branch[1], Tree) : 
                    root = branch[1]
    
                else: 
                    return branch[1]

    # Test the test df against the tree
    correct = 0
    total = 0
    
    for index, row in test.iterrows():
        
        guess = int_test(row)
        
        if guess == row["Survived"]: 
            correct += 1

        total = index
    
    print( correct, "/", total)
    print( correct/total*100, "% correct")



# ============================================================================== Running the code 

# Getting the data into dataframes
train = pd.read_csv("./data/train.csv" )
test = pd.read_csv("./data/test.csv")




# Task 1
# These are the only non-continious ones that are likely to influence the Survival rate - a more comprehesive explanation can be found in the pdf.
attributes_t1 = ['Pclass', 'Sex']

# Passing an empty dataframe as parent_examples for the checks not to throw an error
tree = decisionTreeLearning(train, attributes_t1, pd.DataFrame())

test_tree(tree)
# Running the code





