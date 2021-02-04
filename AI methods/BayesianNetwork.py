from collections import defaultdict

import numpy as np


class Variable:
    def __init__(self, name, no_states, table, parents=[], no_parent_states=[]):
        """
        name (string): Name of the variable
        no_states (int): Number of states this variable can take
        table (list or Array of reals): Conditional probability table (see below)
        parents (list of strings): Name for each parent variable.
        no_parent_states (list of ints): Number of states that each parent variable can take.

        The table is a 2d array of size #events * #number_of_conditions.
        #number_of_conditions is the number of possible conditions (prod(no_parent_states))
        If the distribution is unconditional #number_of_conditions is 1.
        Each column represents a conditional distribution and sum to 1.

        Here is an example of a variable with 3 states and two parents cond0 and cond1,
        with 3 and 2 possible states respectively.
        +----------+----------+----------+----------+----------+----------+----------+
        |  cond0   | cond0(0) | cond0(1) | cond0(2) | cond0(0) | cond0(1) | cond0(2) |
        +----------+----------+----------+----------+----------+----------+----------+
        |  cond1   | cond1(0) | cond1(0) | cond1(0) | cond1(1) | cond1(1) | cond1(1) |
        +----------+----------+----------+----------+----------+----------+----------+
        | event(0) |  0.2000  |  0.2000  |  0.7000  |  0.0000  |  0.2000  |  0.4000  |
        +----------+----------+----------+----------+----------+----------+----------+
        | event(1) |  0.3000  |  0.8000  |  0.2000  |  0.0000  |  0.2000  |  0.4000  |
        +----------+----------+----------+----------+----------+----------+----------+
        | event(2) |  0.5000  |  0.0000  |  0.1000  |  1.0000  |  0.6000  |  0.2000  |
        +----------+----------+----------+----------+----------+----------+----------+

        To create this table you would use the following parameters:

        Variable('event', 3, [[0.2, 0.2, 0.7, 0.0, 0.2, 0.4],
                              [0.3, 0.8, 0.2, 0.0, 0.2, 0.4],
                              [0.5, 0.0, 0.1, 1.0, 0.6, 0.2]],
                 parents=['cond0', 'cond1'],
                 no_parent_states=[3, 2])
        """
        self.name = name
        self.no_states = no_states
        self.table = np.array(table)
        self.parents = parents
        self.no_parent_states = no_parent_states

        if self.table.shape[0] != self.no_states:
            raise ValueError(f"Number of states and number of rows in table must be equal. "
                             f"Recieved {self.no_states} number of states, but table has "
                             f"{self.table.shape[0]} number of rows.")

        if self.table.shape[1] != np.prod(no_parent_states):
            raise ValueError("Number of table columns does not match number of parent states combinations.")

        if not np.allclose(self.table.sum(axis=0), 1):
            raise ValueError("All columns in table must sum to 1.")

        if len(parents) != len(no_parent_states):
            raise ValueError("Number of parents must match number of length of list no_parent_states.")

# Dont do this
# =============================================================================
#     def __str__(self):
#         """
#         Pretty string for the table distribution
#         For printing to display properly, don't use variable names with more than 7 characters
#         """
#         width = int(np.prod(self.no_parent_states))
#         grid = np.meshgrid(*[range(i) for i in self.no_parent_states])
#         s = ""
#         for (i, e) in enumerate(self.parents):
#             s += '+----------+' + '----------+' * width + '\n'
#             gi = grid[i].reshape(-1)
#             s += f'|{e:^10}|' + '|'.join([f'{e + "("+str(j)+")":^10}' for j in gi])
#             s += '|\n'
# 
#         for i in range(self.no_states):
#             s += '+----------+' + '----------+' * width + '\n'
#             state_name = self.name + f'({i})'
#             s += f'|{state_name:^10}|' + '|'.join([f'{p:^10.4f}' for p in self.table[i]])
#             s += '|\n'
# 
#         s += '+----------+' + '----------+' * width + '\n'
# 
#         return s
# =============================================================================

    def probability(self, state, parentstates):
        """
        Returns probability of variable taking on a "state" given "parentstates"
        This method is a simple lookup in the conditional probability table, it does not calculate anything.

        Input:
            state: integer between 0 and no_states
            parentstates: dictionary of {'parent': state}
        Output:
            float with value between 0 and 1
        """
        if not isinstance(state, int):
            raise TypeError(f"Expected state to be of type int; got type {type(state)}.")
        if not isinstance(parentstates, dict):
            raise TypeError(f"Expected parentstates to be of type dict; got type {type(parentstates)}.")
        if state >= self.no_states:
            raise ValueError(f"Recieved state={state}; this variable's last state is {self.no_states - 1}.")
        if state < 0:
            raise ValueError(f"Recieved state={state}; state cannot be negative.")

        table_index = 0
        for variable in self.parents:
            if variable not in parentstates:
                raise ValueError(f"Variable {variable.name} does not have a defined value in parentstates.")

            var_index = self.parents.index(variable)
            table_index += parentstates[variable] * np.prod(self.no_parent_states[:var_index])

        return self.table[state, int(table_index)]


class BayesianNetwork:
    """
    Class representing a Bayesian network.
    Nodes can be accessed through self.variables['variable_name'].
    Each node is a Variable.

    Edges are stored in a dictionary. A node's children can be accessed by
    self.edges[variable]. Both the key and value in this dictionary is a Variable.
    """
    def __init__(self):
        self.edges = defaultdict(lambda: [])  # All nodes start out with 0 edges
        self.variables = {}                   # Dictionary of "name":TabularDistribution

    def add_variable(self, variable):
        """
        Adds a variable to the network.
        """
        if not isinstance(variable, Variable):
            raise TypeError(f"Expected {Variable}; got {type(variable)}.")
        self.variables[variable.name] = variable

    def add_edge(self, from_variable, to_variable):
        """
        Adds an edge from one variable to another in the network. Both variables must have
        been added to the network before calling this method.
        """
        if from_variable not in self.variables.values():
            raise ValueError("Parent variable is not added to list of variables.")
        if to_variable not in self.variables.values():
            raise ValueError("Child variable is not added to list of variables.")
        self.edges[from_variable].append(to_variable)

    # Problem 3a
    # Returns [A B D C]
    def sorted_nodes(self):
        
        def has_incoming_edges(variable):
            
            # Checks if an incoming edge exists. E.g. checks if variables exists within the item of a key
            for node in self.edges:
                if variable in self.edges[node]:
                    return True                
            
            return False
                
        L = []      # Empty list that will contain the sorted elements
        S = []      # Set of all nodes with no incoming edge
        
        # Filling up S with orphans (nodes that have no parents... )        
        for variable_name in self.variables:
            if not self.variables[variable_name].parents :
                S.append(self.variables[variable_name]) 
        
        edges = self.edges.copy()
        
        # While S is not empty
        while S:

            n = S.pop()
            L.append(n)
            
            # Edges are in a form [from node, to node]  <- dont mind this, it is for me
            # Iterating over the edges to find any that start from n 
            for from_node in edges:

                if from_node == n :
                        
                    # Need to make a copy of the list so iteration doesnt fail
                    temp = edges[from_node].copy()
                    
                    # Removing the edge
                    for m in temp:
                        
                        # Removing that edge (from a list which is an item in the dictionary)
                        edges[from_node].remove(m)
                                  
                        # Check if m has any incoming edges
                        if ( not has_incoming_edges(m) ):
                            S.append(m)

        # Dont really need this, but but
        # Check if the graph is acyclic
        for edge_key in edges:
            if ( len ( edges[edge_key] ) != 0 ):                
                    print("Acyclic graph detected!")
                    raise
        return L


class InferenceByEnumeration:
    
    def __init__(self, bayesian_network):
        self.bayesian_network = bayesian_network
        self.topo_order = bayesian_network.sorted_nodes()


    # I started this but never got to finish it
    def _enumeration_ask(self, X, evidence):
        # X - the querry variable
        # E - observed values for variables E
        # Evidence is basicalluy what comes after the pipe, e.g. given, what we know
                
        # Initially empty distribution over X 
        # AKA True and False values for the queary variable X
        Q = [] 
        
        # For True and False (as indicated above)
        for state in (True, False):
            
            # Copying the evidence, so i can add upon it down the line
            # Then it becomes KNOWLEDGE
            knowledge = evidence.copy()
            
            # Is this a good idea?
            # Adding a key with value of X
            knowledge[X] = state
            
            Q.append(self._enumerate_all(self.topo_order, knowledge))
                
        # TODO This needs to be re normalized
        return Q

    def _enumerate_all(self, vars, evidence):
        
        # Get the probability of Y given its parents (can be calculated since evidence about Y is existent/Y's parents are in there)
        def prob(Y, e):

            # If Y has no parents, then we simply use the CPT of Y
            if len(Y.parents_no) == 0:
                if evidence[Y] == 1:
                    return self.bayesian_network.variables[Y.name][0]
                else:
                    return 1 - self.bayesian_network.variables[Y.name][0]
                    
            # If Y does have parents
            else:
                return
        
        # Should sum all the probabilities
        def sum_prob():
            pass
        
        if len(vars) == 0:
            return 1
        
        # Y is unovsorved/hidden variables 
        # It is unobserved list, because evidence AND Y AND X make up the entire domain
        Y = vars[0]

        # The damn book is so badly explained here
        
        # Rest of the unobserved variables list
        Y_rest = vars[1:len(1)]
        
        # If the hidden variable is in the evidence it means we have information on it, so use it down the line
        if Y in evidence:
            return ( prob(Y) * self._enumerate_all(Y_rest, evidence))
        
        # If it is not in the evidence, then we need to use the probability instead
        else:
            return (sum_prob(   ) * self._enumerate_all(Y_rest, evidence.copy()[Y]  ))
            

    def query(self, var, evidence={}):
        """
        Wrapper around "_enumeration_ask" that returns a
        Tabular variable instead of a vector
        """
        q = self._enumeration_ask(var, evidence).reshape(-1, 1)
        return Variable(var, self.bayesian_network.variables[var].no_states, q)




def problem3c():
    
    d1 = Variable('A', 2, [[0.8], [0.2]])
    
    d2 = Variable('B', 2, [[0.5, 0.2],
                           [0.5, 0.8]],
                  parents=['A'],
                  no_parent_states=[2])
    
    d3 = Variable('C', 2, [[0.1, 0.3],
                           [0.9, 0.7]],
                  parents=['B'],
                  no_parent_states=[2])
    
    d4 = Variable('D', 2, [[0.6, 0.8],
                           [0.4, 0.2]],
                  parents=['B'],
                  no_parent_states=[2])


    print(f"Probability distribution, P({d1.name})")
    print(d1)
 
    print(f"Probability distribution, P({d2.name} | {d1.name})")
    print(d2)

    print(f"Probability distribution, P({d3.name} | {d2.name})")
    print(d3)

    print(f"Probability distribution, P({d4.name} | {d2.name})")
    print(d4)


    bn = BayesianNetwork()

    bn.add_variable(d1)
    bn.add_variable(d2)
    bn.add_variable(d3)
    bn.add_variable(d4)
    bn.add_edge(d1, d2)
    bn.add_edge(d2, d3)
    bn.add_edge(d2, d4)

    inference = InferenceByEnumeration(bn)
    posterior = inference.query('C', {'D': 1})
    

    print(f"Probability distribution, P({d3.name} | !{d4.name})")

    print(posterior)
    
    


def monty_hall():
    # Read somewhere on piazza one could turn this in without 4b
    # Dont know if it will work though, but creating a bayesian network from this is relatively straightforward
    
    # The doors
    doors = Variable('Doors', 3, [[1/3], [1/3], [1/3]])
    
    # Guest choice
    guest = Variable('Guest choice', 3, [[1/3],[1/3],[1/3]])
    
    # The host choice variable
    host = Variable('Chosen by host', 3, 
                                [[0, 0, 0, 0, 0.5, 1, 0, 1, 0.5], 
                                [0.5, 0, 1, 0, 0, 0, 1, 0, 0.5],
                                [0.5, 1, 0, 1, 0.5, 0, 0, 0, 0]],
                            ['Doors', 'Guest choice'], [3, 3])
    
    # Create the bayesian network and add the variables
    bn = BayesianNetwork()

    # The vars
    bn.add_variable(doors)
    bn.add_variable(guest)
    bn.add_variable(host)
    
    # The edges
    bn.add_edge(doors, host)
    bn.add_edge(guest, host)

    # Inference
    inference = InferenceByEnumeration(bn)
    posterior = inference.query('Doors', [{'Guest': 0}, {'Host': 0}])


    print(posterior)
    


if __name__ == '__main__':
    problem3c()
    monty_hall()
