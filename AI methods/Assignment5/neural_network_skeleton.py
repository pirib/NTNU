# Use Python 3.8 or newer (https://www.python.org/downloads/)
import unittest
# Remember to install numpy (https://numpy.org/install/)!
import numpy as np
import pickle
import os
import random

# README

# The code is a direct adaptation of the pseudo-code from the book. The naming convention is directly as the notation in the book. 
# Learning rate and number of epochs have been modified to keep the runtime short - around 40 sec for the unittest.


# Custom classes - Neuron and Edge
class Neuron:
    
    def __init__(self, value = None):
        
        # All incomding and outgoing edges are stored as arrays
        self.i_e = []
        self.o_e = []
        
        # a and i_n as defined in the pseudo_code
        self.a = value
        self.i_n = value
        
        # Delta
        self.d = None
           
    # The sigmoid function
    def g(self):
        return 1 /( 1 + np.exp(-self.i_n))
        
    # Derivative of g - g prime
    def gp(self):
        return self.g()*(1-self.g())
    
    # The input function - e.g. the sum of the multuplication between of edges 
    def input_function(self):
        
        # Get the vectors with weights and the activation values from the nodes
        wij = [e.w for e in self.i_e]
        ai  = [e.i.a for e in self.i_e]
        
        # Calculate and return "in"
        return np.dot(wij, ai)

    # Calculate delta for the output layer - using multiplication since there is only one output neuron
    def calc_delta(self, y):
        self.d = self.gp() * (y - self.a)


class Edge:
    
    def __init__(self, i, j):
    
        # Give the weight a random small number between -0.5 and 0.5
        self.w = random.uniform(-0.5, 0.5)
        
        # The i and j neurons that the edge connects
        self.i = i
        self.j = j
        
    # Updates the weight of the edge
    def update_weight(self, d):
        self.w = self.w + d
    

class NeuralNetwork:
    """Implement/make changes to places in the code that contains #TODO."""

    def __init__(self, input_dim: int, hidden_layer: bool) -> None:
        """
        Initialize the feed-forward neural network with the given arguments.
        :param input_dim: Number of features in the dataset.
        :param hidden_layer: Whether or not to include a hidden layer.
        :return: None.
        """

        # --- PLEASE READ --
        # Use the parameters below to train your feed-forward neural network.

        # Number of hidden units if hidden_layer = True.
        self.hidden_units = 25

        # This parameter is called the step size, also known as the learning rate (lr).
        # See 18.6.1 in AIMA 3rd edition (page 719).
        # This is the value of α on Line 25 in Figure 18.24.
        self.lr = 1e-2

        # Line 6 in Figure 18.24 says "repeat".
        # This is the number of times we are going to repeat. This is often known as epochs.
        self.epochs = 128

        # We are going to store the data here.
        # Since you are only asked to implement training for the feed-forward neural network,
        # only self.x_train and self.y_train need to be used. You will need to use them to implement train().
        # The self.x_test and self.y_test is used by the unit tests. Do not change anything in it.
        self.x_train, self.y_train = None, None
        self.x_test, self.y_test = None, None


        # ==============================================================       Initialize the NN
        
        # Hold layers in an array of arrays
        self.layers = []
        
        # Input layer
        self.layers.append( [ Neuron() for n in range(input_dim) ] ) 

        # Hidden layer
        if hidden_layer: self.layers.append( [ Neuron() for n in range(self.hidden_units ) ] ) 
        
        # Output layer
        self.layers.append([Neuron()])

        # Add edges between the neurons
        for li in range(len(self.layers[:-1])):
            for i in self.layers[li]:
                for j in self.layers[li+1]:
                    
                    # Create an edge
                    e = Edge(i,j)
                    
                    # Add the edges to the neurons
                    i.o_e.append(e)
                    j.i_e.append(e)
        
        # Add the bias neurons and their edges
        for l in self.layers[1:]:
            for n in l:
                
                b = Neuron(1)
                e = Edge( b, n)
                b.o_e.append(e)
                n.i_e.append(e)
                

    def load_data(self, file_path: str = os.path.join(os.getcwd(), 'data_breast_cancer.p')) -> None:
        """
        Do not change anything in this method.

        Load data for training and testing the model.
        :param file_path: Path to the file 'data_breast_cancer.p' downloaded from Blackboard. If no arguments is given,
        the method assumes that the file is in the current working directory.

        The data have the following format.
                   (row, column)
        x: shape = (number of examples, number of features)
        y: shape = (number of examples)
        """
        with open(file_path, 'rb') as file:
            data = pickle.load(file)
            self.x_train, self.y_train = data['x_train'], data['y_train']
            self.x_test, self.y_test = data['x_test'], data['y_test']


    def train(self) -> None:
        """Run the backpropagation algorithm to train this neural network"""
        
        # Run through all the training data
        for x, y in zip(self.x_train, self.y_train):
            
            # Calculate all the values in the network 
            self.predict(x)            

            # Train epochs number of times each data sample
            for e in range(self.epochs):
                
                # Calculate output neuron delta
                self.layers[-1][0].calc_delta(y)
                
                # Calculate deltas
                for l in reversed(self.layers[1:-1]):
                    for n in l:
                        n.d = n.gp()*np.dot( [e.w for e in n.o_e], [ e.j.d for e in n.o_e] ) 
                
                # Update weights of every edge in the NN
                for l in self.layers:
                    for n in l:
                        for e in n.o_e:
                            e.update_weight(self.lr*e.i.a*e.j.d)

    def predict(self, x: np.ndarray) -> float:
        
        # Set the values for the input layer
        for n, i in zip(self.layers[0], x):
            n.a = i

        # Forward propagation
        for l in self.layers[1:]:
            for n in l:
                n.i_n = n.input_function()
                n.a = n.g()

        # Calculate the value of the output neuron by backwards iteration
        return self.layers[-1][0].a
        


class TestAssignment5(unittest.TestCase):
    """
    Do not change anything in this test class.

    --- PLEASE READ ---
    Run the unit tests to test the correctness of your implementation.
    This unit test is provided for you to check whether this delivery adheres to the assignment instructions
    and whether the implementation is likely correct or not.
    If the unit tests fail, then the assignment is not correctly implemented.
    """

    def setUp(self) -> None:
        self.threshold = 0.8
        self.nn_class = NeuralNetwork
        self.n_features = 30

    def get_accuracy(self) -> float:
        """Calculate classification accuracy on the test dataset."""
        self.network.load_data()
        self.network.train()

        n = len(self.network.y_test)
        correct = 0
        for i in range(n):
            # Predict by running forward pass through the neural network
            pred = self.network.predict(self.network.x_test[i])
            # Sanity check of the prediction
            assert 0 <= pred <= 1, 'The prediction needs to be in [0, 1] range.'
            # Check if right class is predicted
            correct += self.network.y_test[i] == round(float(pred))
        return round(correct / n, 3)

    def test_perceptron(self) -> None:
        """Run this method to see if Part 1 is implemented correctly."""

        self.network = self.nn_class(self.n_features, False)
        accuracy = self.get_accuracy()
        self.assertTrue(accuracy > self.threshold,
                        'This implementation is most likely wrong since '
                        f'the accuracy ({accuracy}) is less than {self.threshold}.')

    def test_one_hidden(self) -> None:
        """Run this method to see if Part 2 is implemented correctly."""

        self.network = self.nn_class(self.n_features, True)
        accuracy = self.get_accuracy()
        self.assertTrue(accuracy > self.threshold,
                        'This implementation is most likely wrong since '
                        f'the accuracy ({accuracy}) is less than {self.threshold}.')

if __name__ == '__main__':
    unittest.main()



