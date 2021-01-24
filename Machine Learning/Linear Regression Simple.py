import pandas as pd
import matplotlib .pyplot as plt
import numpy as np


# Reading from an excel file
data = pd.read_excel (r'C:\Users\babay\.spyder-py3\Data\data.xlsx')

# Turn the read file into a DataFrame type
# Grabbing the columns I want to use    
df = pd.DataFrame (data, columns=['x1', 'y'])


# This is how you loop through stuff
"""
for index, row in df.iterrows():
    print(row['a']) """
    

# All our x n and theta n
# Trying just with one variable for now. NB! x(0) is always 1
theta = [1,1]

# Hypothesis defined as a linear function accepting a variable var
def hypothesis (var):
    return theta[0] + theta[1] * var

# Decent gradient descent
alpha = 0.001           #Step length

# Running for 400 steps because why not
for i in range(50):

        
    thetaSUM_0 = 0
    # This is the SUM part
    for index, row in df.iterrows():
            thetaSUM_0 =  thetaSUM_0 + ( row['y'] - hypothesis( row['x1'] ) )

    thetaSUM_1 = 0
    # This is the SUM part
    for index, row in df.iterrows():
            thetaSUM_1 =  thetaSUM_1 + ( row['y'] - hypothesis( row['x1'] ) ) * row['x1']


    theta[0] = theta[0] + alpha * thetaSUM_0
    theta[1] = theta[1] + alpha * thetaSUM_1



    # Plotting the linear function
    var = np.linspace(0,1,200)
    y = hypothesis(var)
    
    plt.plot(var, y)

# Plotting the data
plt.plot(df.set_index('x1')['y'], 'ro' , ms = 1)       # Plots open in "Plots" tab!
