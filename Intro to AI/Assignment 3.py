# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    # < ===================================================================================== Me stuff starts here
    
    # Using an argument depth to know how deep in i should search
    # Instead of using the appoach outlined in the book which frankly speaking is a big meh
    # I will call minimax recursively, since it is more... natural this way
    def minimax(self, state, depth, playerIndex):
        # Instead of decrementing depth I decided to increment until i reach the depth of the task
        # This is triggered whenever we are in a terminal state or have reached the depth 
        if depth == self.depth or state.isWin() or state.isLose():
            return [self.evaluationFunction(state), None]
        
        # Packman is player 0, and the maxplayer 
        if playerIndex == 0:
            maxeval = [float('-inf'), None]
            
            # For every legal action run the evaluation min for ghosts, max for pacman
            for action in state.getLegalActions(0):
                evaluation = self.minimax(state.generateSuccessor(0, action), depth, 1)
                
                # Get the max value. The action of the evaluaation variable starts as None (like 123)
                # And we need to save the information about which action gets us the higher value
                if maxeval[0] < evaluation[0]:
                    maxeval = [evaluation[0], action]
        
            return maxeval
        else:
            mineval = [float('inf'), None]
        
            # Same as above, but for ghosts, thus mineval
            for action in state.getLegalActions(playerIndex):
                
                # A bit of embarassing stuff here, but quite readable
                # Instead of creating a nested loop (e.g. for each ghost) I will be recalling the mineval until I run out of ghosts
                if playerIndex+1 < state.getNumAgents():
                    nextAgent = playerIndex+1
                    nextDepth = depth
                else:
                    # I am breaking out of min evaluation 'loop' once it is pacmans turn again
                    nextAgent = 0
                    nextDepth = depth + 1
                
                evaluation = self.minimax(state.generateSuccessor(playerIndex, action), nextDepth, nextAgent)
                
                # Get the min value
                # Same logic as for maxeval
                if mineval[0] > evaluation[0]:
                    mineval = [evaluation[0], action]
        
            return mineval
        


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        # The best_move is basically a pair with the evaluation value and action name
        best_move = self.minimax(gameState, 0 , 0)
        
        # Returning best action move
        return best_move[1]
        
        # I will just comment this out for now
        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    # Since the code is the same before I will just comment out the alpha beta part
    # We take alpha and beta as parameters for bookeping
    # The Maxeval part is commented out, but not the mineval one
    def alphabeta(self, state, depth, playerIndex, alpha, beta):
        if depth == self.depth or state.isWin() or state.isLose():
            return [self.evaluationFunction(state), None]
        
        if playerIndex == 0:
            maxeval = [float('-inf'), None]
            
            for action in state.getLegalActions(0):
                evaluation = self.alphabeta(state.generateSuccessor(0, action), depth, 1, alpha, beta)
                
                if maxeval[0] < evaluation[0]:
                    maxeval = [evaluation[0], action]
                
                # This is basically the only additon worth the mention
                # Updately alpha for the new worst highest value
                alpha = max(evaluation[0], alpha)
                
                # Stop considering this node and all its children
                if beta < alpha:
                    break 

            return maxeval
        
        else:
            mineval = [float('inf'), None]
        
            for action in state.getLegalActions(playerIndex):
                
                if playerIndex+1 < state.getNumAgents():
                    nextAgent = playerIndex+1
                    nextDepth = depth
                else:
                    nextAgent = 0
                    nextDepth = depth + 1
                
                evaluation = self.alphabeta(state.generateSuccessor(playerIndex, action), nextDepth, nextAgent, alpha, beta)
                
                if mineval[0] > evaluation[0]:
                    mineval = [evaluation[0], action]

                beta = min(evaluation[0], beta)

                if beta < alpha:
                    break                
        
            return mineval
        


    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        best_move = self.alphabeta(gameState, 0, 0, float('-inf'), float('inf'))
        return best_move[1]
        #util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
