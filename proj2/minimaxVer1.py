        """
        for i in range self.depth:
          for agentIndex in range gameState.getNumAgents()
            actions = gameState.getLegalActions(agentIndex)
            goalAction = self.evaluationFunction(gameState.generateSuccessor(agentIndex, actions[0]))
            for a in actions[1:]:
            #if 
          
          agentIndex = gameState.getNumAgents()-1
        """
        def maxAgent(gameState, depth):
          if (gameState.isWin()):
            return gameState.getScore()
          actions = gameState.getLegalActions(0);
          bestScore = -99999
          bestAction = Directions.STOP

          for action in actions:
            if (action != Directions.STOP):
              score = minAgent(gameState.generateSuccessor(0, action), depth, 1)
              if (score > bestScore):
                bestScore = score
                bestAction = action

          if (depth == 0):
            #print "best score: ", bestScore
            return bestAction
          else:
            return bestScore

          
        def minAgent(gameState, depth, agentIndex):
          if (gameState.isLose()):
            return gameState.getScore()

          lastAgent = False
          nextAgent = agentIndex + 1
          if (agentIndex == gameState.getNumAgents() -1):
            lastAgent = True
            nextAgent = 0
            
          actions = gameState.getLegalActions(agentIndex);
          bestScore = 99999

          for action in actions:
            if (action != Directions.STOP):
              if (lastAgent):
                if (depth == self.depth - 1):
                  score = self.evaluationFunction(gameState.generateSuccessor(agentIndex, action))
                else:
                  score = maxAgent(gameState.generateSuccessor(agentIndex, action), depth + 1)
              else:
                  score = minAgent(gameState.generateSuccessor(agentIndex, action), depth, nextAgent)
              if (score < bestScore):
                bestScore = score
          return bestScore
        
        return maxAgent(gameState, 0)
