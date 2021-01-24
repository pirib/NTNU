# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:17:09 2021

@author: babay
"""

class Node:
    
    def __init__(self, row, col, grid_size, grid_type):
        # Setting parameters
        self.col = col
        self.row = row
        self.empty = False
        self.neighbours = []        
        
        # Setting neighbours coordinates based on its own col/row and the total size of the grid
        self.set_neighbours(grid_size, grid_type)

    # Set nodes neighbours depending on its placement and total grid_size
    def set_neighbours(self, grid_size, grid_type):

        # Helper tuples indicating possible neighours' outset
        offset_triangle = ( (-1,-1) , (0,-1) , (-1,0) , ( 0, 1) , ( 1, 0) , (1, 1) )
        offset_diamond =  ( ( 0,-1) , (1,-1) , (1, 0) , (-1, 0) , (-1, 1) , (0, 1) )
                
        if grid_type == 0 :
        
            # Checking each possible neighbour based on the offset
            for o in offset_diamond:
                # If it is a diamond, then it is a piece of cake
                # For each possible neighbour, e.g. coordinates of the created node + offset check if it stays within the bounds of the grid_size
                
                # Potential neighbour coordinates
                pot_n = [self.row + o[0], self.col + o[1]]
                
                if ( 0 <= pot_n[0] < grid_size and 0 <= pot_n[1] < grid_size):
                    self.neighbours.append( pot_n )        
        else:
            for o in offset_diamond:
                
                  pot_n = [self.row + o[0], self.col + o[1]]
                  
                  if ( 0 <= pot_n[0] < grid_size and 0 <= pot_n[1] <= self.col + 1):
                    self.neighbours.append( pot_n )
            
        print(self.neighbours)  