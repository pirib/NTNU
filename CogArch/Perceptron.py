"""
@author: pirib
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

# Truth table (aka training data) for AND, OR and XOR gates, with inputs and the correct "label"
tt_AND = (  (0,0,0),
            (0,1,0),
            (1,0,0),
            (1,1,1)  )

tt_OR = (   (0,0,0),
            (0,1,1),
            (1,0,1),
            (1,1,1)  )

tt_XOR = (  (0,0,0),
            (0,1,1),
            (1,0,1),
            (1,1,0)  )

# Training data for Iris 
data = pd.read_csv('data.csv')

tt_iris = []

for index, row in data.iterrows():
        tt_iris.append(row.to_list())


class Perceptron:
    
    weights = [0,0]     # A list with weights of the inputs. There are just two in this case, since we are doing AND, OR, XOR, and petal/sepal thing.
    threshold = 0       # The threshold of the nuron that needs to be surpassed for neuron to fire. 
    
    bias = 0           # The bias of the neuron

    alpha = 0.01       # Basically the step taken in the correct direction during the training (comes from ML). Has been periodically adjusted to get the best results
    
    # Prints out the information about the Perceptron, for debugging purposes
    def print(self):
        print("Weights are: " + str(self.weights))
        print("Bias is: " + str(self.bias))
        
    # Tests perceptron using some training data. Returns number of correctly predicted data sets.
    def test(self, data):
        num_correct = 0
        for row in data:
            if self.activate(row[0:len(row)-1]) == row[len(row)-1]:
                num_correct += 1
        
        print("Total correct: " + str(num_correct) + "/" + str(len(data)))

    # Calculates the total value in the neuron and fires if it is above the threshold
    def activate(self, inputs):
        
        # Sum is the sum of the synapses weight multiplied by the input value
        Sum = self.bias

        # Multiply each input with the currently stored weight        
        Sum += np.dot( self.weights, inputs ) 
        
        # Return 1 if Neuron fires, 0 if it does not
        if Sum >= self.threshold:
            return 1
        else:
            return 0
            
    # Train the neuron with data data (expect a list with n weights and correct label)
    def train(self, data):
        for i in range(100):    
            for row in data:  # Will train once per row in the data
                
                # Get the result according to the current weights and bias in the neuron
                current_result = self.activate(row[0:len(row)-1])
                
                # Adjust the bias of the neuron
                self.bias += self.alpha * (row[len(row)-1] - current_result)
                 
                # Adjusting the weights of the synapses i have (which is -1 since the last value is the label)
                it = 0
                for i in row[0:len(row)-1]:
                    self.weights[it] += self.alpha * (row[len(row)-1] - current_result) * i
                    it += 1
           
      
print("AND gate")              
# Instantiate
AND = Perceptron()
# Train
AND.train(tt_AND)
# Show the values inside
AND.print()
# Test
AND.test(tt_AND)

print("OR gate")              
# Instantiate
OR = Perceptron()
# Train
OR.train(tt_OR)
# Show the values inside
OR.print()
# Test
OR.test(tt_OR)

print("XOR gate")              
# Instantiate
XOR = Perceptron()
# Train
XOR.train(tt_XOR)
# Show the values inside
XOR.print()
# Test
XOR.test(tt_XOR)

print("IRIS")              
# Instantiate
IRIS = Perceptron()
# Train
IRIS.train(tt_iris)
# Show the values inside
IRIS.print()
# Test
IRIS.test(tt_iris)

# Lets try plotting stuff

# Virginica and Versicolor
x1 = []
y1 = []

# Setosa
x2 = []
y2 = []

# Plotting!
for i in tt_iris:
    if i[2] == 0:
        x1.append(i[0])
        y1.append(i[1])
    else:
        x2.append(i[0])
        y2.append(i[1])
        
        
plt.scatter(x1,y1,marker='+' )
plt.scatter(x2,y2,marker='x' )

x = np.linspace(2,5, 200)
def y(x):
    return (-IRIS.bias - IRIS.weights[0]*x)/IRIS.weights[1]

plt.plot( x, y(x) )































