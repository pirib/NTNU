# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:15:44 2021

@author: babay
"""

import actor_critic as ac
import grid


import matplotlib.pyplot as plt

class RL():
    
    # Private members
    
    actor = None
    critic = None
    state = None
    
    
    # Analytics 
    solved_puzzles = [0]
    
    def __init__(self, grid_type, grid_size, episodes = 500):
        self.grid_type = grid_type
        self.grid_size = grid_size
        self.episodes = episodes
        self.train()
        
        
    def train(self):
        
        # Initializing the actor and the critic 
        self.actor = ac.Actor()
        self.critic = ac.Critic()
        

        # Start looping for eacn number of episodes
        for episode in range(self.episodes):
                    
            # Getting the initial state 
            # The initial action is decided via the policy by the actor
            self.state = grid.Grid(self.grid_type, self.grid_size) 

            solved = False
            
            # Clearing eligibility traces
            self.actor.clear_elig()
            self.critic.clear_elig()
            
            # Playing and learning until a terminal state is reached
            while (not self.state.is_terminal()):

                # Take the action 
                s, sp, r = self.actor.play(self.state)
                
                # Let the critic evaluate
                td = self.critic.evaluate(s, sp, r)
                
                # Update all the visited saps for actor and v(s) for the critic
                self.actor.update_visited(td)
                self.critic.update_visited(td)

                if (r > 0):
                    solved = True
        
            if (solved):
                self.solved_puzzles.append(  self.solved_puzzles[-1] + 1  )
            else:
                self.solved_puzzles.append(  self.solved_puzzles[-1]  )
        
        plt.plot( range(self.episodes+1), self.solved_puzzles)
            
        
        
    # Play the game greedily, e.g. full on greed policy
    # TODO this is shit, doesnt work, some code needs to be rewamped
    def play(self, episodes=1):
        for e in range(episodes):
            g = grid.Grid(self.grid_type, self.grid_size)
            
            while(not g.is_terminal()):
                g.make_move(self.actor.play(g, True))
    
    
test = RL(0,4)




