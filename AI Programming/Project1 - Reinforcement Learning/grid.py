# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 14:07:25 2021

@author: babay
"""

# In-house stuff
import node as N

# For general funciton
import random

# For printing pretty stuff
import networkx as nx
import matplotlib.pyplot as plt 



class Grid():

    # Private
    grid = []
    
    # Potential neighbours set for each node - (row, col)
    offset = ( (-1,-1) , (0,-1) , (-1,0) , ( 0, 1) , ( 1, 0) , (1, 1) )

    # Methods
    # Initialize the grid. grid_type - 0 for diamond, 1 for triangle
    # Size is as defined in hex-board-games.pdf
    def __init__(self, grid_type, size, point_num = 1):
        self.create(grid_type, size)
        self.create_start_points(point_num)
        
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
                # Make a new node and shove into the right column. The node is then accessible at grid[c][r].
                self.grid[r].append( N.Node(r,c,size, grid_type) )

        # The nodes are generated, so it is time to set its neighbours
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

    # Initializes empty points in the grid
    def create_start_points(self, point_num):
                
        num = point_num
        
        while (num > 0):
            # Initialize a random starting point        
            random_node = random.choice( random.choice(self.grid) )
            
            if (random_node.empty == False):
                random_node.empty = True
                num -=  1

    # Returns a dictionary of available actions given a grid (e.g. state)
    def available_actions(self):
        # For each empty node check along the 6 edges, with 2 depth, ensure that the one in between is filled.
        actions = {}
        
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
                            print(pmv)
                            
                            # We are looking at the node 1 step further in, which should be a neighbour of the n. If it isnt, then we are outside the grid.
                            # That node should also not be empty, since that is the node we will be considering to move the peg from.
                            try:
                                # Check if that node is filled (and, well exists), as well as make sure that the coordinates are not negative
                                if ( not self.grid[pmv[0]][pmv[1]].empty and pmv[0] >= 0 and pmv[1] >= 0 ):
                                    actions[ pmv[0], pmv[1] , node.row, node.col ] = ""
                                    
                            except:
                                pass
        
        # Returning the dictionary of actions
        return actions    

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
        # TODO: Sometimes the graph looks ... scrambled. Find out how to keep the lines parallel        
        
        nx.draw(G, labels, labels=labels, node_color=color_map)
        plt.show()



    # For Debugging purposes
    
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
        
    
    
    
    
test = Grid(0,4)

test.print_grid()

print(test.available_actions())