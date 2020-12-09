from iceWorld import IceWorld
import numpy as np
import random
import sys

class QLearningSolver:
    def __init__(self,iceWorld:IceWorld):
        self.iceWorld = iceWorld
        self.epsilon = 0.05
        self.discountFactor = 0.9
        self.learningRate = 0.1
        self.worldDimension = self.iceWorld.getDimension()
        self.nStates = self.worldDimension[0] * self.worldDimension[1]
        self.nActions = len(self.iceWorld.actions)
        self.qTable = np.zeros((self.nStates,self.nActions))
        self.trajectoriesWithoutChangeToStop = 10000

    def stateTupleToStateValue(self,stateTuple):
        return stateTuple[0] * stateTuple[1]
    def stateValueToStateTuple(self,stateValue):
        row = int(stateValue/self.worldDimension[1])
        col = stateValue % self.worldDimension[1]
        if row == self.worldDimension[0]-1:
            return (row,col,True)
        else:
            return (row, col, False)

    def selectBestActionIndex(self,currentState,possibleActionIndices):
        stateValue = self.stateTupleToStateValue(currentState)
        maximizingIndex = np.argmax(self.qTable[stateValue,possibleActionIndices])
        bestActionIndex = possibleActionIndices[maximizingIndex]
        return bestActionIndex

    def updateQTable(self,state,actionIndex,nextState,reward):
        stateValue = self.stateTupleToStateValue(state)
        nextStateValue = self.stateTupleToStateValue(nextState)
        optimalFutureValueEstimate = np.max(self.qTable[nextStateValue])
        oldQValue = self.qTable[stateValue][actionIndex]
        temporalDifference = reward + self.discountFactor * optimalFutureValueEstimate - oldQValue
        self.qTable[stateValue][actionIndex] = oldQValue + self.learningRate * temporalDifference

    def doTrajectory(self) -> int:
        accumulatedRewards = 0
        currentState = (0,0,False)
        isTerminal = currentState[2]
        while not isTerminal:
            possibleActionIndices = self.iceWorld.getPossibleActionIndices(currentState)
            if np.random.rand() <self.epsilon:
                actionIndex = random.choice(possibleActionIndices)

            else:
                actionIndex = self.selectBestActionIndex(currentState,possibleActionIndices)
            action = self.iceWorld.actions[actionIndex]
            nextState,reward = self.iceWorld.performAction(currentState,action)
            accumulatedRewards += reward
            self.updateQTable(currentState,actionIndex,nextState,reward)
            currentState = nextState
            isTerminal = currentState[2]
        return accumulatedRewards

    def getOptimalTrajectory(self):
        currentState = (0, 0, False)
        isTerminal = currentState[2]
        trajectory = []
        while not isTerminal:
            possibleActionIndices = self.iceWorld.getPossibleActionIndices(currentState)

            actionIndex = self.selectBestActionIndex(currentState, possibleActionIndices)
            action = self.iceWorld.actions[actionIndex]
            if self.iceWorld.performAction(currentState, action) is None:
                print("Hallo")
            nextState, reward = self.iceWorld.performAction(currentState, action)
            trajectory.append((currentState, action, nextState, reward))
            currentState = nextState
            isTerminal = currentState[2]

        return trajectory

    def solve(self):
        #solve until hit polar bears is not decreasing for at least 10 trajectories
        accumulatedRewards = - sys.maxsize -1
        nTrajectoriesWithoutChange = 0
        while nTrajectoriesWithoutChange < self.trajectoriesWithoutChangeToStop:
            currentAccumulatedRewards = self.doTrajectory()
            if currentAccumulatedRewards > accumulatedRewards:
                accumulatedRewards = currentAccumulatedRewards
                nTrajectoriesWithoutChange = 0
            else:
                nTrajectoriesWithoutChange += 1
            print(f"Current number of polar bears hit: {-accumulatedRewards}")
            if currentAccumulatedRewards == 0:
                break






