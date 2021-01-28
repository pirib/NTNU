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
    
    offset = ( (-1,-1) , (0,-1) , (-1,0) , ( 0, 1) , ( 1, 0) , (1, 1) )

    # Methods
    # Initialize the grid. grid_type - 0 for diamond, 1 for triangle
    # Size is as defined in hex-board-games.pdf
    def __init__(self, grid_type, size, point_num = 3):
        self.create(grid_type, size)
        self.create_start_point(point_num)

    def create(self, grid_type, size):
        
        # Initial, e.g. the first row of the grid - it is the same as size for diamond and 0 for the triangle (meaning there will be one "starting" node)
        init_size = size if grid_type == 0 else 0
            
        # Creating nodes
        for c in range(size):
            # Create a new empty row
            self.grid.append([])
                
            # Increase the row by 1 if we are creating a triangle board
            if (grid_type == 1): init_size = init_size + 1
            
            for r in range (init_size):
                # Make a new node and shove into the right column. The node is then accessible at grid[c][r].
                self.grid[c].append( N.Node(r,c,size, grid_type) )

        # The nodes are generated, so it is time to set its neighbours
        for row in self.grid:
            for node in row:
                for o in self.offset:
                    
                    # Potential neighbour coordinates
                    p_n_r = node.row + o[0]
                    p_n_c = node.col + o[1]
                    
                    # As long as potential coordinates are not negative (since Python allows using negative indexes...)
                    if p_n_c >= 0 and p_n_r >= 0:
                        
                        try:
                            node.neighbours.append( self.grid[p_n_c][p_n_r] )
                        except:
                            pass                 


    def create_start_point(self, point_num):
                
        num = point_num
        
        while (num > 0):
            # Initialize a random starting point        
            random_node = random.choice( random.choice(self.grid) )
            
            if (random_node.empty == False):
                random_node.empty = True
                num -=  1


    def print_grid(self):
        
        # The new graph for printing
        G = nx.Graph()

        # The colors used in the drawing
        color_map = []

        # Iterate through all the nodes, and add them as.. nodes
        for row in self.grid:
            for n in row:
                G.add_node(n) 
                color_map.append('black') if n.empty else color_map.append('blue')
        
        # Iterate through each neighbour of the node, and add the edges in between. Networkx ignores already existing edges, which is nice
        for row in self.grid:
            for node in row:
                for n in node.neighbours:
                    G.add_edge(node, n)
        
        # Draws the nodes 
        # TODO: Sometimes the graph looks ... scrambled. Find out how to keep the lines parallel        
        
        nx.draw(G, node_color=color_map)
        plt.show()
        
        # https://networkx.org/documentation/stable/tutorial.html#drawing-graphs

    # Debug
    
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
        
    
    
    
    
test = Grid(1,3)
test.print_simple()
test.print_neighbours()

test.print_grid()
