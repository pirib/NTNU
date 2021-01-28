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
        self.neighbours = list()        
        

    # Set nodes neighbours depending on its placement and total grid_size
    def set_neighbours(self, neighbours):
        self.neighbours = neighbours
        
    
    # Debug methods
    def print_neighbours(self):
        for n in self.neighbours:
            print(n.col, n.row, " ", end = "")
        print()

