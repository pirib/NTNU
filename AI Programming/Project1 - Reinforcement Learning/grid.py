# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 14:07:25 2021

@author: babay
"""

# In-house stuff
import node as N

# For general funciton
import random
import time

# For printing pretty stuff
import networkx as nx
import matplotlib.pyplot as plt 



class Grid():

    # Private
    grid = []
    
    # Potential neighbours set for each node - (row, col)
    offset = ( (-1,-1) , (0,-1) , (-1,0) , ( 0, 1) , ( 1, 0) , (1, 1) )

    # Methods
    
    # Grid:
    # Initialize the grid. grid_type - 0 for diamond, 1 for triangle
    # Size is as defined in hex-board-games.pdf
    
    # Starting points

    # start_point_num - number of starting points. Should be equal to the number 
    # start_point_coor - coordinates of the starting points, expects a list of lists. If None is passed then starting points are created randomly within the grid.
        
    # Example
    # Grid(0,5, start_point_coor = [ [1,1] ] )
    # Will create a 5-size diamond grid with a peg missing at [1,1] <- Note how this was passed!    
    
    def __init__( self, grid_type, size, start_point_num = 1, start_point_coor = None ):
        self.grid.clear()
        self.create(grid_type, size)
        self.create_start_points(start_point_num, start_point_coor)

        
    # Destructor - also removes all the nodes.
    def __del__(self): 
        for row in self.grid:
            for node in row:
                del node
        
        del self
        
        
    # Creates the grid
    def create(self, grid_type, size):
        
        # Initial, e.g. the first row of the grid - it is the same as size for diamond and 0 for the triangle (meaning there will be one "starting" node)
        init_size = size if grid_type == 0 else 0
            
        # Creating nodes
        for r in range(size):
            # Create a new empty row
            self.grid.append([])
                
            # Increase the row by 1 if we are creating a triangle board
            if (grid_type == 1): init_size = init_size + 1
            
            for c in range (init_size):
                # Make a new node and shove into the right row. The node is then accessible at grid[r][c].
                self.grid[r].append( N.Node(r,c,size, grid_type) )

        # Setting nodes neighbours
        
        # For each node in the grid, check if there is a neighbour in one of the possible offset coordinates
        for row in self.grid:
            for node in row:
                for o in self.offset:
                    
                    # Potential neighbour row/col coordinates
                    p_n_r = node.row + o[0]
                    p_n_c = node.col + o[1]
                    
                    # As long as potential coordinates are not negative (since Python allows usage negative indexes...)
                    if p_n_c >= 0 and p_n_r >= 0:
                        
                        try:
                            node.neighbours.append( self.grid[p_n_r][p_n_c] )
                        except:
                            pass                 


    # Initializes empty points in the grid. These are the "starting points" for the game.

    # Deliverable note
    # Starting in 1 2 or 2 1 in a 4 size diamond yields no solutions.
    def create_start_points(self, point_num, points_coor):
    
        # If no point_coordinates have been passed, the points are generated randomly   
        # Number of points generates deoends on point_num
        if points_coor == None:
        
            while (point_num > 0):
                # Initialize a random starting point        
                random_node = random.choice( random.choice(self.grid) )
                
                if (random_node.empty == False):
                    random_node.empty = True
                    point_num -=  1
            
        # If coordinates have been provided, then they become the starting points instead
        # The parameters point_num is ignored
        else:
            
            # Python's way of handling lists made me do this
            coordinates = [ [None, None] ]
            coordinates.append( points_coor )
            
            for coor in points_coor:
                if ( coor[0] != None):
                    self.grid[coor[0]][coor[1]].empty = True     
                
                
    # Pass an action in the form of a [ (from_node) , (over_node) , (to_node)  ]
    # The function moves the grid into a new state
    def make_move(self, action):
        if action in self.get_available_actions():
            
            f_node_coor    = action[0]
            over_node_coor = action[1]
            to_node_coor   = action[2]            
            
            from_node = self.grid[f_node_coor[0]][f_node_coor[1]]
            over_node = self.grid[over_node_coor[0]][over_node_coor[1]]
            to_node   = self.grid[to_node_coor[0]][to_node_coor[1]]
            
            from_node.empty = True
            over_node.empty = True
            to_node.empty   = False
            
        else: 
            raise Exception("Attempted to make an illegal move! Move is: " + action)


    # Returns a compact state representation 
    def get_state(self, binary = True):
        """
        # The binary state representation
        state = ''
        
        for row in self.grid:
            for node in row:
                state = state + '0' if node.empty else state + '1'
        """
        
        state = []
        
        for row in self.grid:
            for node in row:
                state.append( 0 if node.empty else 1)
        
        return tuple(state)
        


    # Returns a dictionary of available actions given a grid (e.g. state)
    def get_available_actions(self):
        # For each empty node check along the 6 edges, with 2 depth, ensure that the one in between is filled.
        actions = []
        
        # Iterate through all the nodes
        for row in self.grid:
            for node in row:
                
                # Find an empty one
                if (node.empty):
                    
                    # Check each non-empty neighbour
                    for n in node.neighbours:
                        if (not n.empty):
                            # Find the offset (e.g. show on which edge we should look 1 more deeper to find a potential move)
                            offset = [n.row - node.row, n.col - node.col]
                            
                            # Could potentiall make a move from these coordinates
                            pmv = [ n.row + offset[0] , n.col + offset[1]]
                            
                            # We are looking at the node 1 step further in, which should be a neighbour of the n. If it isnt, then we are outside the grid.
                            # That node should also not be empty, since that is the node we will be considering to move the peg from.
                            try:
                                # Check if that node is filled (and, well exists), as well as make sure that the coordinates are not negative
                                if ( not self.grid[pmv[0]][pmv[1]].empty and pmv[0] >= 0 and pmv[1] >= 0 ):
                                    
                                    # Action representation from node n0, over node n1, to node n2
                                    
                                    action_representation = ((pmv[0], pmv[1]), (n.row, n.col), (node.row, node.col))
                                    
                                    actions.append(action_representation)
                                    
                            except:
                                pass
        
        # Returning the dictionary of actions
        return tuple(actions)


    # Returns True if there are no more moves left to do (e.g. the terminal state)
    def is_terminal(self):
        return not bool(self.get_available_actions())


    # Returns number of remaining pegs
    def remaining_pegs(self):
        num_peg = 0
        for row in self.grid:
            for node in row:
                if (not node.empty):
                    num_peg += 1
        return num_peg

    # The environment returns 100 if the terminal state reached is a solved puzzle, and 0 otherwise
    # TODO return minus for bad states
    def get_reward(self):         
        return 100 if (self.remaining_pegs() == 1) else 0

    
    # Prints out a pretty looking grid
    def print_grid(self):
        
        # The new graph for printing
        G = nx.Graph()

        # The colors and labels used in the drawing
        color_map = []
        labels = {}

        # Iterate through all the nodes, and add them as.. nodes
        for row in self.grid:
            for n in row:
                G.add_node(n) 
                color_map.append('red') if n.empty else color_map.append('green')
                labels[n] = [n.row, n.col]
                
        # Iterate through each neighbour of the node, and add the edges in between. Networkx ignores already existing edges, which is nice
        for row in self.grid:
            for node in row:
                for n in node.neighbours:
                    G.add_edge(node, n)
        
        # Draws the nodes 
    
        nx.draw(G, labels, labels=labels, node_color=color_map)
        plt.show()


    # For Debugging =============================================================
    
    # Gives a nice little representation of the grid
    def print_simple(self):
        for row in self.grid:
            for node in row:
                print("*", end = "")
            print()


    # Prints every Node's neigbhours in the grid
    def print_neighbours(self):
        for row in self.grid:
            for n in row:
                n.print_neighbours()
        
    
    # End of the Class =============================================================
    


# Plays a game randmoly picking available actions
# This is for fun
def random_play():
    play = Grid(0,4)
    
    while ( not play.is_terminal() ):
        play.make_move( random.choice(  play.get_available_actions()  )  )
        play.print_grid()
        time.sleep(0.5)
        
    del play


