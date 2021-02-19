# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:15:44 2021

@author: babay
"""

import actor_critic as ac
import grid

import matplotlib.pyplot as plt

import time

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
                 create_within_coor = False,
                 
                 # Training Param
                 train_episodes = 1000, 
                 
                 # Actor params
                 actor_learning_step = 0.01, 
                 actor_greed_rate = 0.8, 
                 actor_greed_decay = False,
                 actor_elig_rate = 0.9, 
                 actor_discount = 0.9,
                 
                 # Critic params
                 critic_mode = 0,                                   # 0 for tabular, 1 for neural nets 
                 critic_nn_layers = [1],                            # Number of neurons per hidden layer
                 critic_learning_step = 0.01, 
                 critic_elig_rate = 0.9, 
                 critic_discount = 0.9,

                 
                 # Analytics
                 print_grid_train = False,
                 print_grid_play = False
                 ):
        
        # Grid related
        self.grid_type = grid_type
        self.grid_size = grid_size
        self.start_point_num = start_point_num
        self.start_point_coor = start_point_coor
        self.create_within_coor = create_within_coor 
        
        # Training related
        self.episodes = train_episodes
        
        # Actor params
        self.actor_learning_step = actor_learning_step  
        self.actor_greed_rate = actor_greed_rate
        self.actor_greed_decay = actor_greed_decay 
        self.actor_elig_rate = actor_elig_rate
        self.actor_discount = actor_discount
        
        # Critic params
        self.critic_mode = critic_mode 
        self.critic_learning_step = critic_learning_step
        self.critic_elig_rate = critic_elig_rate 
        self.critic_discount = critic_discount 
        
        critic_nn_layers.insert(0 , grid_size * grid_size if grid_type == 0 else grid_size*(grid_size + 1) / 2) 
        self.critic_nn_layers = critic_nn_layers                    # Calculate number of neurons in input layer
        
        # Analytics
        self.print_grid_train = print_grid_train
        self.print_grid_play = print_grid_play
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
            self.state = grid.Grid(self.grid_type, self.grid_size, self.start_point_num, self.start_point_coor, self.create_within_coor) 
            
            # Clearing eligibility traces
            self.actor.clear_elig()
            self.critic.clear_elig()
            
            # Analytics
            #print(f"Currently on episode {episode+1}")
            #self.state.print_grid(episode)
                        
            # Greed Decay
            if self.actor_greed_decay:
                
                # self.actor.greed_rate = 1/ math.log(math.e + (1/500)*(episode))              # Really slow decay
                # self.actor.greed_rate = 1 / (episode/(self.episodes/100) + 1)                # Medium decay
                self.actor.greed_rate = self.actor.greed_rate*0.99
                
            # Playing and learning until a terminal state is reached
            while (not self.state.is_terminal()):
                    
                # Take the action 
                s, sp, r = self.actor.play(self.state)
                
                # Let the critic evaluate
                td = self.critic.evaluate(s, sp, r)
        
                # Update all the visited saps for actor and v(s) for the critic
                self.actor.update_visited(td)
                self.critic.update_visited(td)
                
                # Grid printing
                if self.print_grid_train: self.state.print_grid(episode)
                
            # Analytics
            if (self.state.remaining_pegs() == 1):
                total_solved.append( total_solved[-1] + 1 )
                episodes_run.append( episode )
            
            pegs_remaining.append( self.state.remaining_pegs() )
        
        
        # Analytics
        
        # Plots the total solved vs episodes run
        plt.figure(2)
        plt.plot( episodes_run, total_solved )
        
        plt.xlabel("Episodes")
        plt.ylabel("Solved")

        # Plots the number of pegs remaining per episode
        plt.figure(3)
        plt.plot( range(len(pegs_remaining)) , pegs_remaining )
        
        plt.xlabel("Episode")
        plt.ylabel("Pegs left on the board")
        plt.show()
        
        
    # Play the game greedily, e.g. use the deterministic policy
    def play(self, episodes=50, print_grid = False, speed = 0.5):

        solved = 0

        for e in range(episodes):
            g = grid.Grid(self.grid_type, self.grid_size, self.start_point_num, self.start_point_coor, self.create_within_coor)
            
            while(not g.is_terminal()):
                g.make_move(self.actor.det_policy( g ))
                if print_grid: 
                    self.state.print_grid(e)
                    time.sleep(speed)
                    
            if g.remaining_pegs() == 1:
                solved += 1
          
        print(solved, "/", episodes)
    

# Deliverables

"""
# Problem 2
problem2 = RL(
        # 5 size triangle
        grid_type = 1, 
        grid_size = 5, 
        
        # Starting points
        start_point_coor= [ [2,1] ],                       #  Other starting points are [3,1], [3,2]

        # Actor params
        actor_learning_step = 0.9, 
        actor_greed_decay = True,                          # Check line 127 for the decay rate formula
        actor_elig_rate = 0.9, 
        actor_discount = 0.9,
        
        # Critic params
        critic_mode = 1,                                   # 0 for tabular, 1 for neural nets 
        critic_learning_step = 0.1, 
        critic_elig_rate = 0.9, 
        critic_discount = 0.9,


        # Training parameters
        train_episodes = 100
        )

problem2.play(100)

# Play one game while printing out the grids, with half a second delay
problem2.play(1, True, 0.5)
"""

"""
# Problem 3
# Starting in 2 1 and 1 2 in a 4 size diamond yields no solutions. That is why roughly half of the played games will not be solved
problem3 = RL(
        # 4 size rombus
        grid_type = 0, 
        grid_size = 4, 
        
        # Starting points
        start_point_coor= [ [1,1] ],                        # The other starting coordinates are [1,2], [2,1], [2,2]
        
         # Actor params
        actor_learning_step = 0.1, 
        actor_greed_rate = 1, 
        actor_greed_decay = True,                         
        actor_elig_rate = 0.9, 
        actor_discount = 0.9,
        
        # Critic params
        critic_mode = 0,                                   # 0 for tabular, 1 for neural nets 
        critic_learning_step = 0.1, 
        critic_elig_rate = 0.9, 
        critic_discount = 0.9,


        # Training parameters
        train_episodes = 600
    
    )

problem3.play(100)
"""


"""
rl = RL(
        # Grid related parameters
        grid_type = 0, 
        grid_size = 4, 
        
        start_point_coor= [ [1,1] ],
        
        # Actor params
        actor_learning_step = 0.1, 
        actor_greed_rate = 0.1, 
        actor_greed_decay = False,
        actor_elig_rate = 0.9, 
        actor_discount = 0.9,
        
        # Critic params
        critic_mode = 1,                                   # 0 for tabular, 1 for neural nets 
        critic_nn_layers = [4, 4],  
        
        critic_learning_step = 0.1, 
        critic_elig_rate = 0.9, 
        critic_discount = 0.9,

        train_episodes = 50,
        
    )


rl.play()
"""