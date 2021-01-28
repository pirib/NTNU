# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 14:07:25 2021

@author: babay
"""

import node as N


class Grid():

    # Private
    grid = []
    
    # Helper tuples indicating possible neighours' offsets [row, col]
    offset_triangle = ( (-1,-1) , (0,-1) , (-1,0) , ( 0, 1) , ( 1, 0) , (1, 1) )
    offset_diamond =  ( ( 0,-1) , (1,-1) , (1, 0) , (-1, 0) , (-1, 1) , (0, 1) )

    offset = ( (-1,-1) , (0,-1) , (-1,0) , ( 0, 1) , ( 1, 0) , (1, 1) )

    # Methods
    # Initialize the grid. grid_type - 0 for diamond, 1 for triangle
    # Size is as defined in hex-board-games.pdf
    def __init__(self, grid_type, size):
        self.create(grid_type, size)
        

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
                            # TODO for some reason this appends a Node wrapped in a list 
                            node.neighbours.append( self.grid[p_n_c][p_n_r] )
                        except:
                            pass
                        

    # Debug
    
    # Gives a nice little representation of the grid
    def print_grid(self):
        for row in self.grid:
            for node in row:
                print("*", end = "")
            print()

    # Prints every Node's neigbhours in the grid
    def print_neighbours(self):
        for row in test.grid:
            for n in row:
                n.print_neighbours()
        
    
    
    
    
test = Grid(0,2)
test.print_grid()

test.print_neighbours()


