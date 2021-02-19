# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:17:09 2021

@author: babay
"""

class Node:
    
    # check out bit board
    
    def __init__(self, row, col, grid_size, grid_type):
        # Setting parameters
        self.col = col
        self.row = row
        self.empty = False
        self.neighbours = []      
        

    # Set nodes neighbours depending on its placement and total grid_size
    def set_neighbours(self, neighbours):
        self.neighbours = neighbours
        
    def remove_pin(self):
        self.empty = True
        
    def insert_pin(self):
        self.empty = False
    
    # Debug methods
    def print_neighbours(self):
        for n in self.neighbours:
            print(n.col, n.row, " ", end = "")
        print()
