# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 14:07:25 2021

@author: babay
"""

import node as N


class Grid():

    # Private
    grid = []

    # Methods
    # Initialize the grid. grid_type - 0 for diamond, 1 for triangle
    # Size is as defined in hex-board-games.pdf
    def __init__(self, grid_type, size):
        self.make_grid(grid_type, size)
        

    def make_grid(self, grid_type, size):
        
        # Initial, e.g. the first row of the grid - it is the same as size for diamond and 0 (e.g. 1) for the triangle
        init_size = size if grid_type == 0 else 0
                
        for c in range(size):
            # Create a new empty row
            self.grid.append([])
                
            # Increase the row by 1 if we are creating a triangle board
            if (grid_type == 1): init_size = init_size + 1
            
            for r in range (init_size):
                # Make a new node and shove into the right column. The node is then accessible at grid[c][r].
                self.grid[c].append( N.Node(r,c,size, grid_type) )
                
                
    # Helpers
    def print_grid(self):
        for row in self.grid:
            for node in row:
                print(node.neighbours)
                
            print()

    
test = Grid(1,4)
#test.print_grid()