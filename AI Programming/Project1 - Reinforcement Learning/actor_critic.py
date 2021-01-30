# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 18:52:41 2021

@author: babay
"""
import random


class Critic():
    
    # Private
    # The structure is state = value, eligibility, visited this episode (Bool)
    state_value = {} 
    
    td = None
    
    # Constructor
    # Mode: 0 for tabular, 1 for neural network
    # TODO Mode doesnt do shit yet
    def __init__(self, mode = 0, learning_step = 0.1, elig_rate = 0.5, discount = 0.09):
        
        # Setting the private parameters
        self.mode = mode
        self.learning_step = learning_step
        self.elig_rate = elig_rate
        self.discount = discount
       
        # Cleaning up the old state values
        self.state_value.clear()
        
    # Sets all eligibility rates in the dictionary to 0
    def clear_elig(self):
        for key in self.state_value:
            self.state_value[key][1] = 0
            self.state_value[key][2] = False
            
            
    # Add a v(s) if it hasnt been visited before, and give it a random small number
    # TODO ehhh, like this? ^
    def add_vs(self, s):   
        if (not s in self.state_value):
            self.state_value[s] = [ random.random() , 0, False] 
    
    # Returns value of a state, e.g. V(S)
    def v(self, state):
        return self.state_value[state][0]
   
    # Calculates the delta
    def calculate_td(self, s, sp, r):
        self.td = r + self.discount*self.v(sp) - self.v(s)
   
    # The Evaluation step, right after Actor has made a move and transition s -> sp has occured
    def evaluate(self, s, sp, r):
        
        # Add a new state s
        # TODO do i need to add sp as well?
        self.add_vs(s)
        self.add_vs(sp)
        
        # Calculate TD
        self.calculate_td(s, sp ,r)
    
        # Update the eligibility for s
        self.state_value[ s ][ 1 ] = 1
        self.state_value[ s ][ 2 ] = True

        return self.td
        
    def update_visited(self, td):
        for key in self.state_value:
            if (self.state_value[key][2] == True):
                self.state_value[key][0] = self.state_value[key][0] + self.learning_step*td*self.state_value[key][1]
                self.state_value[key][1] = self.state_value[key][1]*self.discount*self.elig_rate
            
class Actor():
    
    # Private
    # This is where State action pair along the eligibility traces are kept
    # The structure is state, action = value, eligibility, visited this episode (Bool)
    saps = {}
    
    
    # S and Sp (S prime dont judge me), initialized as empty
    s = None
    sp = None
    
    
    # Constructor
    def __init__(self, learning_step = 0.01, greed_rate = 0.1 , elig_rate = 0.5, discount = 0.09):
        
        # Setting the private parameters
        self.learning_step = learning_step
        self.greed_rate = greed_rate
        self.elig_rate = elig_rate
        self.discount = discount
        
        # Cleaning up the old sap values
        self.saps.clear()
    
    
    # Sets all eligibilirt rates in the dictionary to 0
    # Also sets, visited this episode to 0
    def clear_elig(self):
        for key in self.saps:
            self.saps[key][1] = 0
            self.saps[key][2] = False
    
        
    # TODO change this so the values are normalised and it becomes a prob distribution
    # Current policy - returns an action based on e-greedy algorithm    
    def policy(self, state, exploit):
        
        # With a random chance greed_rate explore instead of exploit
        if (random.random() < self.greed_rate and not exploit ):
            # Exploration choice
            return tuple( random.choice(state.get_available_actions()) )
        
        # Exploit move
        else:
            highest_a = float('-inf')
            result = None
            s = state.get_state()
            

            for a in state.get_available_actions():
                if ( self.saps[s,a][0] > highest_a):
                    highest_a = self.saps[s,a][0]
                    result = a

            return tuple(result)

    
    # Adds a sap if it didnt exist before
    def add_saps(self, state):   
        s = state.get_state()
        actions = state.get_available_actions()
        
        for a in actions:
            if (not (s,a) in self.saps):
                self.saps[s,a] = [0,0,False]
                             
       
    # The actor plays, e.g. takes a turn, e.g. moves a peg
    def play(self, state, exploit = False):
        
        # Get the current state reprersentation
        s = state.get_state()

        # We are about to play from a state
        # Need to add current state s, and all possible actions a into the saps
        self.add_saps(state)
        
        # Let the policy decide on the action
        a = self.policy(state, exploit)
        
        # Update the eligibility for s,a
        self.saps[s,a][1] = 1  # THIS DOESNT EXIST!
        self.saps[s,a][2] = True
        
        # Perform that action, thus moving to a new state 
        state.make_move(a)
        
        # Get the new state info
        sp = state.get_state()
        
        # Give it a reward of 100, if we reached the terminal state with one peg left (e.g. solved the puzzle)
        # Otherwise zero, including if we reached the terminal state with more than one peg
        r = state.get_reward()
        
        return s, sp, r
        
    
    # Update the visited saps with new elig. traces, and values
    def update_visited(self, td):
        for key in self.saps:
            if (self.saps[key][2] == True):
                self.saps[key][0] = self.saps[key][0] + self.learning_step*td*self.saps[key][1]
                self.saps[key][1] = self.saps[key][1]*self.discount*self.elig_rate
            
    
    