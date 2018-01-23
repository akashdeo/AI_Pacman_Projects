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
        #description given in the better evaluation function#
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScore = successorGameState.getScore()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print successorGameState
        #print newPos
        #print newFood
        #print newGhostStates
        #print newScaredTimes
        "*** YOUR CODE HERE ***"
        ghostposition = currentGameState.getGhostPosition(1)
    	ghostDistance=util.manhattanDistance(ghostposition, newPos)
    	score=max(ghostDistance,4)
    	score+=newScore
    	foodlist=newFood.asList()
    	closestfood=100#took 100 as i don't think i have to concentrate on food that are more than 100 score away from the given pacman position,its about the closestFood which is at least distance#
    	for foodpos in foodlist:
          distance=util.manhattanDistance(foodpos,newPos)
          if (distance<closestfood):
            closestfood = distance
        score-=closestfood
        return score

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
        import sys#it is for -infinity and +infinity values#
        def max(gameState,depthOfTree):
            if depthOfTree == self.depth:
                return (self.evaluationFunction(gameState),None)#even if its the leaf node,we got to return some action with it becuaes of the user defined structure of function#
            actions=gameState.getLegalActions(0)#0 indicates it is of pacman#
            value=-sys.maxint#This is the way of getting the minimum value possible in python#
            action1=None
            valueActionTuple=(value,action1)
            if len(actions)==0:#if no actions,return the current score with null as action#
                return (self.evaluationFunction(gameState),None)
            for action in actions:
                nextState=gameState.generateSuccessor(0, action)
                nextStateScore,action1=min(nextState, 1, depthOfTree)
                if (nextStateScore>value):
                    value= nextStateScore
                    action1=action
                    valueActionTuple=(value,action1)#this is important as it is not only the score which we require but we require the action as our final answer#
            return valueActionTuple
        def min(gameState,agentNo,depthOfTree):
            actions=gameState.getLegalActions(agentNo)#here for the first time agent 1 actions will be taken#
            value=sys.maxint#select maximum value in python#
            action1=None
            valueActionTuple = (value,action1)
            if len(actions)==0:#if there are no actions that can be taken,then we have to leave everything on that position's score!!#
                return (self.evaluationFunction(gameState),None)
            for action in actions:
                nextState=gameState.generateSuccessor(agentNo, action)
                if (agentNo==gameState.getNumAgents()-1):#if this condition is satisfied then it means that all ghosts are at the moment over,its time to go to max node again#
                    nextStateScore,action1=max(nextState,depthOfTree+1)
                elif(agentNo!=(gameState.getNumAgents()-1)):
                       nextStateScore,action1=min(nextState,agentNo+1,depthOfTree)#this means there are more than 1 ghost in the problem who is trying to minimize utility value of pacman#
                if (nextStateScore<value):
                    value=nextStateScore
                    action1=action
                    valueActionTuple=(value,action1)
            return valueActionTuple
        def minimax(gameState):   
            finalValue,finalAction=max(gameState,0)#starting from depth 0,i.e top down approach as expected in the question#
            return finalAction#final action taken#
        finalAction=minimax(gameState)
        return finalAction   
        util.raiseNotDefined() 

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self,gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"#this code is quite similar to the above minimax function but only two global values alpha and beta are taken for the purpose of pruning#
        import sys#it is for -infinity and +infinity values#
        alpha=-sys.maxint
        beta=sys.maxint
        def maxalphabeta(gameState,depthOfTree,alpha,beta):
            if depthOfTree==self.depth:
                return (self.evaluationFunction(gameState),None)#even if its the leaf node,we got to return some action with it because of the user defined structure of function#
            actions=gameState.getLegalActions(0)#0 indicates it is of pacman#
            value=-sys.maxint#This is the way of getting the minimum value possible in python#
            action1=None#its important as this value is required to set its initial action#
            valueActionTuple=(value,action1)
            if len(actions)==0:
                return (self.evaluationFunction(gameState),None)
            for action in actions:
            	if(alpha>beta):#pruning condition,that means less nodes to visit!!#
                  return valueActionTuple
                nextState=gameState.generateSuccessor(0, action)
                nextStateScore,action1=minalphabeta(nextState, 1, depthOfTree,alpha,beta)
                if(nextStateScore>value):
                    value=nextStateScore
                    action1=action
                    valueActionTuple=(value,action1)#this is important as it is not only the score which we require but we require the action as our final answer#
                if(value>beta):
                  return valueActionTuple
                alpha=max(alpha,value)  #maximizing the value of alpha#     
            return valueActionTuple
        def minalphabeta(gameState,agentNo,depthOfTree,alpha,beta):
            actions=gameState.getLegalActions(agentNo)#here for the first time agent 1 actions will be taken#
            value=sys.maxint#for min value we always select +infinity#
            action1 = None
            valueActionTuple=(value,action1)
            if len(actions)==0:#if there are no actions that can be taken,then we have to leave everything on that position's score!!#
                return (self.evaluationFunction(gameState),None)
            for action in actions:
            	if(alpha>beta):#pruning condition,that means less nodes to visit!!#
                  return valueActionTuple
                nextState=gameState.generateSuccessor(agentNo, action)
                if (agentNo==gameState.getNumAgents() - 1):#if this condition is satisfied then it means that all ghosts are now over,its time to go to max node again#
                    nextStateScore,action1=maxalphabeta(nextState,depthOfTree+1,alpha,beta)
                elif(agentNo!=(gameState.getNumAgents()-1)):
                    nextStateScore,action1=minalphabeta(nextState,agentNo+1,depthOfTree,alpha,beta)#this means there are more than 1 ghost in the problem who is trying to minimize utility value of pacman#
                if (nextStateScore<value):
                    value=nextStateScore
                    action1=action
                    valueActionTuple=(value,action1)
                if(value<alpha):#we always want to increase the value of alpha
                  return valueActionTuple
                beta=min(beta,value) #as we want to decrease the value of beta     
            return valueActionTuple
        def alphabetapruning(gameState,alpha,beta):   
            finalValue,finalAction=maxalphabeta(gameState,0,alpha,beta)#starting from depth 0,i.e top down approach as expected in the question#
            return finalAction#final action taken#
        finalAction=alphabetapruning(gameState,alpha,beta)
        return finalAction    
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self,gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        import sys#it is for -infinity and +infinity values#
        def max(gameState,depthOfTree):
            if depthOfTree==self.depth:
                return (self.evaluationFunction(gameState),None)#even if its the leaf node,we got to return some action with it because of the user defined structure of function#
            actions=gameState.getLegalActions(0)#0 indicates it is of pacman#
            value=-sys.maxint#This is the way of getting the minimum value possible in python#
            action1=None
            valueActionTuple=(value,action1)
            if len(actions)==0:
                return (self.evaluationFunction(gameState),None)
            for action in actions:
                nextState=gameState.generateSuccessor(0,action)
                nextStateScore,action1=equalChanceNodes(nextState,1,depthOfTree)
                if (nextStateScore>value):
                    value=nextStateScore
                    action1=action
                    valueActionTuple=(value,action1)#this is important as it is not only the score which we require but we require the action as our final answer#
            return valueActionTuple
        def equalChanceNodes(gameState,agentNo,depthOfTree):
            actions=gameState.getLegalActions(agentNo)#here for the first time agent 1 actions will be taken#
            value=0#for min value we always select 0 instead of infinity#
            action1 = None#always the natural action must be null#
            tScore=0
            valueActionTuple=(value,action1)
            if len(actions)==0:#if there are no actions that can be taken,then we have to leave everything on that position's score!!#
                return (self.evaluationFunction(gameState),None)
            for action in actions:
                nextState=gameState.generateSuccessor(agentNo,action)
                if(agentNo==gameState.getNumAgents()-1):#if this condition is satisfied then it means that all ghosts are now over,its time to go to max node again#
                    nextStateScore,action1=max(nextState,depthOfTree+1)
                elif(agentNo!=(gameState.getNumAgents()-1)):
                    nextStateScore,action1=equalChanceNodes(nextState,agentNo+1,depthOfTree)#this means there are more than 1 ghost in the problem #
                tScore+=nextStateScore
                value=tScore/len(actions)#equal probability#
                valueActionTuple=(value,action1)
            return valueActionTuple
        def expectimax(gameState):   
            finalValue,finalAction=max(gameState,0)#starting from depth 0,i.e top down approach as expected in the question#
            return finalAction#final action taken#
        finalAction=expectimax(gameState)
        return finalAction    
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <it is the same as i did in reflexAction,the difference is just that used currentGameState.getScore() as a parameter than the successorGameState.getScore()(luck factor was there,because i used permutations of scores and saw that barring fewcases,pacman wins in most of the cases)
      also to live away from the ghost i assumed that we have 4 positions through which ghost can come to eat the pacman,so i took the maximum of ghost score and 4(4 ways to attack the pacman,(left,right,down,up) and used as a parameter,
      closest food distance is subtracted in order to eat the food.>
    """
    "*** YOUR CODE HERE ***"
    import sys
    newPos=currentGameState.getPacmanPosition()
    newFood=currentGameState.getFood()
    newGhostStates=currentGameState.getGhostStates()
    newScore=currentGameState.getScore()
    newScaredTimes=[ghostState.scaredTimer for ghostState in newGhostStates]
    ghostposition=currentGameState.getGhostPosition(1)
    ghostDistance=util.manhattanDistance(ghostposition, newPos)
    score=max(ghostDistance,4)
    score=score+newScore
    foodlist=newFood.asList()
    closestfood=100
    for foodpos in foodlist:
        distance = util.manhattanDistance(foodpos,newPos)
        if (distance<closestfood):
                closestfood=distance
    score=score-closestfood   
    return score
    util.raiseNotDefined()
# Abbreviation
better = betterEvaluationFunction

