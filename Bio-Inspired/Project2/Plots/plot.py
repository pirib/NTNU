
"""
Created on Mon Mar  8 10:35:16 2021

@author: babay
"""

import networkx as nx
import matplotlib.pyplot as plt 

# Open and read the file
file = open("plot", "r")
raw_data = file.read().split("/")


# Handling data

plot_data = []



# Make a list of lists
for depot in raw_data:
    plot_data.append(depot.split("\n"))

# Clean up
del file
del raw_data

# Remove the last element, which is an empty list
plot_data.pop()

# Remove the last element in each depot (useless)
for depot in plot_data:
    depot.pop()


# Parse data into easy access
depots_id = []
depots_coord = []

for depot in plot_data:
    depots_id.append( int(depot[0].split()[0]) )
    depots_coord.append( (int(depot[0].split()[1]) ,int(depot[0].split()[2]) ))
    
# Parsing customer data
customer_id = []
customer_coord = []
    
for depot in plot_data:
    for customer in depot[1:]:
        customer_id.append( int(customer.split()[0] ) )
        customer_coord.append( (int(customer.split()[1]), int(customer.split()[2]) )  )
        
# Clean up
del customer
del depot
del plot_data


# Plotting!

G = nx.Graph()

color_map = []
labels = {}

for depot, coor in zip(depots_id, depots_coord):
    G.add_node(depot)
    color_map.append('red')
    labels[depot] = coor
    
for customer, coor in zip(customer_id, customer_coord):
    G.add_node(customer)
    color_map.append('blue')
    labels[customer] = coor

nx.draw(G,labels, node_color = color_map, node_size = 50)














