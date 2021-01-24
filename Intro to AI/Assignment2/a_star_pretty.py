# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 17:51:38 2020

@author: babay

I have not coded in Python for a long time now so please pardon my code
Swapping the argument on line 14 from 1 to 5 and just running the code will do the trick

"""

import Map as mp

# Instantiate the map
map = mp.Map_Obj(1)

# Some handlers to make my life easier
start = map.get_start_pos()
goal = map.get_goal_pos()

# Frontier + visited cells
OPEN = []
CLOSED = []


# Eucldidian distance between position1 p1 and position2 p2, aka heursitic funciton
def h(p1, p2):

    # Calculate x and y
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]

    return (x**2 + y**2)**0.5

# Magic happens here
def a_star():
    
    # These are my "nodes". Tried implementing with OOP but oh boy is it terrible in python
    # own coordinates, parent coordinates, cost f
    c = [ start, start, 0 ]     # c stands for current cell
        
    # Our starting frontier is the start cell
    OPEN.append(c)
    
    # MAGIC TIME!
    # Looping until we find the cell of which f(n) = 0, or in my case, coordinates fit with the goal
    while c[0] != goal:
        
        # basically marking the current node as visited
        CLOSED.append(c[0])
        
        # Grabbing the neighbours
        # Do not hate me for this please. Basically moving +-1 in x/y coordinate space one at a time.
        n_top = [ c[0][0] , c[0][1] - 1 ]
        n_bot = [ c[0][0] , c[0][1] + 1 ]
        n_lef = [ c[0][0] - 1 , c[0][1] ]
        n_rig = [ c[0][0] + 1 , c[0][1] ]
        
        # Making sure these neighbours are not walls and are not in the visited list
        if map.get_cell_value(n_top) != -1 and n_top not in CLOSED:
            OPEN.append( [ n_top , c, c[2] + map.get_cell_value(n_top) + h(n_top, start) ] )
        if map.get_cell_value(n_bot) != -1 and n_bot not in CLOSED:
           OPEN.append( [ n_bot , c, c[2] + map.get_cell_value(n_bot) + h(n_bot, start) ] )
        if map.get_cell_value(n_lef) != -1 and n_lef not in CLOSED:
           OPEN.append( [ n_lef , c, c[2] + map.get_cell_value(n_lef) + h(n_lef, start) ] )    
        if map.get_cell_value(n_rig) != -1 and n_rig not in CLOSED:
            OPEN.append( [ n_rig, c, c[2] + map.get_cell_value(n_rig) + h(n_rig, start) ] )  
         
        # Running through the frontier, looking for shortest distance cell that is not in the visited nodes
        # Temp massive value
        shortest_distance = [[-1,-1], [-1,-1], 999999 ]
        
        for n in OPEN:
            if n[2] < shortest_distance[2] and n[0] not in CLOSED:
                shortest_distance = n
        
        c = shortest_distance

    # once the while loop is finished running it means the shortest path has been found
    # just need to walk "backwards" my looking at its parents starting from the goal node
    while c[0] != start:
        map.replace_map_values(c[0],9,goal)
        c = c[1]


# Run the algorithm
a_star()

# aaaaaand show the map!
map.show_map()
         
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        