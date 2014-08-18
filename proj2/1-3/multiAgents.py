# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        
        finalScore = 0.0 + successorGameState.getScore()
        
        closestFoodDist = 100000.0
        manDis = 0.0
        totManDist = 1.0
        for p in newFood.asList():
            manDis = manhattanDistance(newPos,p)
            totManDist += manDis
            if manDis < closestFoodDist:
              closestFoodDist = manDis
          
        finalScore += 1/(closestFoodDist*closestFoodDist)  + 1/totManDist
                
        for s in newGhostStates:
          ghostDist = manhattanDistance(newPos,s.getPosition())
          if ghostDist < 6 and ghostDist > s.scaredTimer:
            finalScore -= 1/(ghostDist*ghostDist)
              
        return finalScore

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
        """
        "*** YOUR CODE HERE ***"
        return self.maximizer(gameState, self.depth, 1)[0]

    #get alternatively recursive call
    def maximizer(self, gameState, depth, numPacmans):
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return (None, self.evaluationFunction(gameState))
        
        #get pacman actions and successor gamestates
        actions = gameState.getLegalActions(0)
        newGameStates = [gameState.generateSuccessor(0, action) for action in actions]
        
        #call minimizer for each newGameState
        #every node consists of (action, score)
        newChildNodes = [self.minimizer(newGameState, depth-1, newGameState.getNumAgents()-1) for newGameState in newGameStates]

        #return the node with hight score (action, score)
        newScores = [newChildNode[1] for newChildNode in newChildNodes]
        result = (actions[newScores.index(max(newScores))], max(newScores))
        return result


    #get recursively call for each ghost
    #on finishing, call maximizer
    def minimizer(self, gameState, depth, numGhosts):
        if gameState.isWin() or gameState.isLose():
          return (None, self.evaluationFunction(gameState))
        elif numGhosts == 1:
          func = lambda x, y, z: self.maximizer(x, y, z) 
        else: 
          func = lambda x, y, z: self.minimizer(x, y, z)
        
        #get ghost actions and successor gamestates
        actions = gameState.getLegalActions(numGhosts)
        newGameStates = [gameState.generateSuccessor(numGhosts, action) for action in actions]


        #call minimizer for each newGameState with ghosts left
        #call maximizer for newGameState with no ghost left
        #every node consists of (action, score)
        newChildNodes = [func(newGameState, depth, numGhosts-1) for newGameState in newGameStates]
        
        #return the node with lowest score (action, score)
        newScores = [newChildNode[1] for newChildNode in newChildNodes]

        result = (actions[newScores.index(min(newScores))], min(newScores))
        return result


         
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.maximizer(gameState, self.depth, 1, float("-inf"), float("inf"))[0]
        
            #get alternatively recursive call
    def maximizer(self, gameState, depth, numPacmans, alpha, beta):
        if depth == 0 or gameState.isWin() or gameState.isLose():
          return (None, self.evaluationFunction(gameState))
        
        result = (None,float("-inf"))
        
        #get pacman actions and successor gamestates
        actions = gameState.getLegalActions(0)
        newGameStates = {}
        newGameStateList = []
        for action in actions:
          newGameState = gameState.generateSuccessor(0, action)
          tempResult = self.minimizer(newGameState, depth-1, newGameState.getNumAgents()-1, alpha, beta)
          if tempResult[1] > result[1]:
            result = (action,tempResult[1])
          if tempResult[1] > beta:
            return result
          alpha = max(alpha, result[1])

        #return the node with hight score (action, score)
        #newScores = [newChildNode[1] for newChildNode in newChildNodes]
        #result = (actions[newScores.index(max(newScores))], max(newScores))
        return result


    #get recursively call for each ghost
    #on finishing, call maximizer
    def minimizer(self, gameState, depth, numGhosts, alpha, beta):
        if gameState.isWin() or gameState.isLose():
          return (None, self.evaluationFunction(gameState))
        
        result = (None, float("inf"))
        
        if numGhosts == 1:
          func = lambda v, w, x, y, z: self.maximizer(v, w, x, y, z) 
        else: 
          func = lambda v, w, x, y, z: self.minimizer(v, w, x, y, z)
        
        #get ghost actions and successor gamestates
        actions = gameState.getLegalActions(numGhosts)
        newGameStates = {}
        for action in actions:
          newGameState = gameState.generateSuccessor(numGhosts, action)
          tempResult = func(newGameState, depth, numGhosts-1, alpha, beta)
          if tempResult[1] < result[1]:
            result = (action, tempResult[1])
          if result[1] < alpha:
            return result
          beta = min(beta, result[1])

        #call minimizer for each newGameState with ghosts left
        #call maximizer for newGameState with no ghost left
        #every node consists of (action, score)
     ###########
          
        #return the node with lowest score (action, score)
        #newScores = [newChildNode[1] for newChildNode in newChildNodes]

        #result = (actions[newScores.index(min(newScores))], min(newScores))
        return result

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

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

