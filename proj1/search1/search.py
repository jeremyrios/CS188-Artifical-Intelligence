# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

from util import *

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    
    "*** YOUR CODE HERE ***"
    #initialzation
    nodes_stack = Stack()
    actions_stack = Stack()
    start_state = problem.getStartState()
    fringe_closed = (start_state,)
    for suc in problem.getSuccessors(start_state):
      nodes_stack.push(suc)

    #flag for deadend
    flag_deadend = True
    prev_state = start_state
    
    #main loop
    while True:
      #if all paths are exhausted
      if nodes_stack.isEmpty():
        print "Fail to find goal state"
        return None
      #get new node
      node = nodes_stack.pop()
      #test for goal state
      if problem.isGoalState(node[0]):
        break;
      
      #not the goal
      if not node[0] in fringe_closed:
        #set flag False whenever a new node shows up
        #store the previous state for possible deadend
        flag_deadend = False
        prev_state = node[0]
        #put the node back and record the path
        nodes_stack.push(node)
        actions_stack.push(node[1])
        #store the fringe and expand the node
        fringe_closed += (node[0],)
        #insert nodes, also check against fringe_closed
        for suc in problem.getSuccessors(node[0]):       
          if not suc[0] in fringe_closed:
            nodes_stack.push(suc)
      else:
        #set flag True on seeing the prev state
        if prev_state == node[0]:
          flag_deadend = True
        #if seen a deadend&state in closed,
        #delete the stop
        if flag_deadend:
          actions_stack.pop()
    
    #add the final path and return
    actions_stack.push(node[1])
    return actions_stack.list

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    #initialization
    nodes_queue = Queue()
    actions_queue = Queue()
    start_state = problem.getStartState()
    fringe_closed = []
    nodes_queue.push(start_state)
    actions_queue.push([])
    
    #Main Loop
    while True:
      if nodes_queue.isEmpty():
        print "Failed to find the goal path"
        return None
      #FIFO
      node = nodes_queue.pop()
      action = actions_queue.pop()
      #check for goal state
      if problem.isGoalState(node):
        return action

      #if not goal
      if not node in fringe_closed:
        successors = problem.getSuccessors(node)
        fringe_closed += [node]
        #reach a new cornor
        #clear all queues, only remember the last node
        for suc in successors:
          #if not suc[0] in fringe_closed:
          nodes_queue.push(suc[0])
          actions_queue.push(action + [suc[1]])


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #initialization
    nodes_heapq = PriorityQueue()
    actions_heapq = PriorityQueue()
    start_state = problem.getStartState()
    fringe_closed = ()
    nodes_heapq.push(start_state, 0)
    actions_heapq.push([], 0)

    #Main Loop
    while True:
      if nodes_heapq.isEmpty():
        print "Failed to find the goal path"
        return None
      #FIFO
      node = nodes_heapq.pop()
      action = actions_heapq.pop()
      #check for goal state
      if problem.isGoalState(node):
        return action

      #if not goal
      if not node in fringe_closed:
        fringe_closed += (node,)
        for suc in problem.getSuccessors(node):
          if not suc[0] in fringe_closed:
            nodes_heapq.push(suc[0], suc[2])
            actions_heapq.push(action + [suc[1]], suc[2])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    #initialization
    nodes_heapq = PriorityQueue()
    actions_heapq = PriorityQueue()
    start_state = problem.getStartState()
    fringe_closed = ()
    nodes_heapq.push((start_state,0), 0+heuristic(start_state,problem))
    actions_heapq.push([], 0+heuristic(start_state, problem))

    #Main Loop
    while True:
      if nodes_heapq.isEmpty():
        print "Failed to find the goal path"
        return None
      #FIFO
      node = nodes_heapq.pop()
      action = actions_heapq.pop()
      #check for goal state
      if problem.isGoalState(node[0]):
        return action

      #if not goal
      if not node[0] in fringe_closed:
        fringe_closed += (node[0],)
        for suc in problem.getSuccessors(node[0]):
          if not suc[0] in fringe_closed:
            f = node[1] + suc[2]
            cost = f + heuristic(suc[0], problem)
            nodes_heapq.push((suc[0], f) , cost)
            actions_heapq.push(action + [suc[1]], cost)
            #print "Nodes:  " + str(suc[0]) + " Cost: " + str(cost)
            #print "actions: " + str(action+[suc[1]]) + "Cost: "
            #print "**********************************"


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
