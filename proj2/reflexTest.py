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
        
        newGhostPositions = successorGameState.getGhostPositions()
        "*** YOUR CODE HERE ***"
        """
        #return successorGameState.getScore()
        def surroundingGhosts(ghostList, curPos, radius=2):
          curX,curY = curPos
          allGhosts = {}
          sGhosts = []
          for ghost in ghostList:
          ### map ghosts positions to ghost obj
            allGhosts[ghost.getPosition()] = ghost
        
          checkPos = []
          for x in range(curX-radius,curX+radius+1):
            if x == curX:
              for y in range(curY-radius, curY+radius+1):
                checkPos += [(x,y)]
            else:
              checkPos += [(x,curY)]
          for pos in checkPos:
            if pos[0] and pos[1] >= 0:
              if pos in allGhosts:
                sGhosts += [allGhosts[pos]]

          return sGhosts
        """
        closestFoodDist = 1000.0
        manDis = 0.0
        for p in newFood.asList():
            manDis += manhattanDistance(newPos,p)
            if manDis < closestFoodDist:
              closestFoodDist = manDis
          
        ghostPenelty = 0.0
        
        '''
        surroundingPositions = [(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1),(x-1,y),(x-1,y+1)]
        radius = 1
        for x in range(newPos[0]-radius,newPos[0]+radius+1):
          if x == curX:
            for y in range(newPos[1]-radius, newPos[1]+radius+1):
              checkPos += [(x,y)]
        '''
        
        for s in newGhostStates:
          ghostDist = manhattanDistance(newPos,s.getPosition())
          if ghostDist < 3:
            if ghostDist > s.scaredTimer:
              ghostPenelty = (1/ghostDist)*10
        """
        #//G_PENALTY = -30
        #//finalScore = successorGameState.getScore()

        ###print "" ### DEBUG
        ###print successorGameState
        ###print "ghost states: ", newGhostStates
        sg = surroundingGhosts(newGhostStates,newPos)
        ###if sg != []: print "found ghosts: ", sg
        ###
        for g in sg:
          if g.scaredTimer == 0:
            ###print "first finalscore", finalScore
            finalScore += G_PENALTY
            ###print "final finalscore", finalScore
        ###print "returning score: ",finalScore
        ###util.pause()

        return finalScore
        """
        return (1/closestFoodDist) - ghostPenelty
