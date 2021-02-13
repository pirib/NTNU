# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:15:44 2021

@author: babay
"""

import actor_critic as ac
import grid


import matplotlib.pyplot as plt

class RL():
    
    # Once RL is initalized, so will these.
    actor = None
    critic = None
    state = None
    
    def __init__(self, 
                 
                 # Grid params
                 grid_type, 
                 grid_size, 
                 start_point_num = 1, 
                 start_point_coor = None, 
                 
                 # Training Param
                 train_episodes = 1000, 
                 
                 # Actor params
                 actor_learning_step = 0.1, 
                 actor_greed_rate = 0.1, 
                 actor_elig_rate = 0.9, 
                 actor_discount = 0.09,
                 
                 # Critic params
                 critic_mode = 0,                           # 0 for tabular, 1 for neural nets 
                 critic_nn_layers = [10, 20, 10],           # Number of neurons per hidden layer
                 critic_learning_step = 0.1, 
                 critic_elig_rate = 0.9, 
                 critic_discount = 0.09,

                 
                 # Analytics TODO unused so far
                 print_grid = False
                 ):
        
        # Grid related
        self.grid_type = grid_type
        self.grid_size = grid_size
        self.start_point_num = start_point_num
        self.start_point_coor = start_point_coor
        
        # Training related
        self.episodes = train_episodes
        
        # Actor params
        self.actor_learning_step = actor_learning_step  
        self.actor_greed_rate = actor_greed_rate
        self.actor_elig_rate = actor_elig_rate
        self.actor_discount = actor_discount
        
        # Critic params
        self.critic_mode = critic_mode 
        self.critic_learning_step = critic_learning_step
        self.critic_elig_rate = critic_elig_rate 
        self.critic_discount = critic_discount 
        
        critic_nn_layers.insert(0 , grid_size * grid_size if grid_type == 0 else grid_size(grid_size + 1) / 2) 
        self.critic_nn_layers = critic_nn_layers  # Calculate number of neurons in input layer
        
        # Analytics
        self.print_grid = print_grid
        
        # Train the RL
        self.train()
        
     
    # Train the RL
    def train(self):
        
        # Initializing the actor and the critic 
        self.actor = ac.Actor(
                learning_step = self.actor_learning_step, 
                greed_rate = self.actor_greed_rate, 
                elig_rate = self.actor_elig_rate, 
                discount = self.actor_discount
            )
                
        self.critic = ac.Critic(
            mode = self.critic_mode, 
            learning_step = self.critic_learning_step, 
            elig_rate = self.critic_elig_rate, 
            discount = self.critic_discount,
            critic_nn_layers = self.critic_nn_layers
            )
        
        # Analytics
        total_solved = [ 0 ]
        episodes_run = [ 0 ]
        pegs_remaining = [ ]
        
        # Start looping for eacn number of episodes
        for episode in range(self.episodes):
                    
            # Getting the initial state 
            # The initial action is decided via the policy by the actor
            self.state = grid.Grid(self.grid_type, self.grid_size, self.start_point_num, self.start_point_coor) 
            
            # Clearing eligibility traces
            self.actor.clear_elig()
            self.critic.clear_elig()
            
            # Testing Grounds ==============
            # Greed rate changes depending on the number of episodes run
            # Results in higher number of solved puzzles, but also means less exploration
            # TODO find the one that uses ln() in the book
            # self.actor.greed_rate = 1/(1 + episode)**0.5              
            # Testing Grounds ==============
            
            # Playing and learning until a terminal state is reached
            while (not self.state.is_terminal()):
                    
                # Take the action 
                s, sp, r = self.actor.play(self.state)
                
                # Let the critic evaluate
                td = self.critic.evaluate(s, sp, r)
        
                # Update all the visited saps for actor and v(s) for the critic
                self.actor.update_visited(td)
                self.critic.update_visited(td)
                
                
            # Analytics
            if (self.state.remaining_pegs() == 1):
                total_solved.append( total_solved[-1] + 1 )
                episodes_run.append( episode )
            
            pegs_remaining.append( self.state.remaining_pegs() )
        
        
        # Analytics
        
        # Plots the total solved vs episodes run
        plt.figure()
        plt.plot( episodes_run, total_solved )
        
        plt.xlabel("Episodes")
        plt.ylabel("Solved")

        # Plots the number of pegs remaining per episode
        plt.figure()
        plt.plot( range(len(pegs_remaining)) , pegs_remaining )
        
        plt.xlabel("Episode")
        plt.ylabel("Pegs left on the board")
        
        
    # Play the game greedily, e.g. use the deterministic policy
    def play(self, episodes=50):

        solved = 0
        
        for e in range(episodes):
            g = grid.Grid(self.grid_type, self.grid_size, self.start_point_num, self.start_point_coor)
            
            while(not g.is_terminal()):
                g.make_move(self.actor.det_policy( g ))
            
            if g.remaining_pegs() == 1:
                solved += 1
          
        print(solved, "/", episodes)
    
    
    
# Time to run the function

rl = RL(
        # Grid related parameters
        grid_type = 0, 
        grid_size = 4, 
        start_point_coor= [ [1,1] ],
        
        critic_mode = 0,
        
        actor_greed_rate = 0.1, 

        train_episodes = 100
    )



rl.play()
