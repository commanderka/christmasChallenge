import numpy as np
from termcolor import colored


def splitWordIntoChars(word):
    return [ord(char) for char in word]


class IceWorld:
    def __init__(self,polarBearChar='#', emptyCellChar="."):
        self.polarBearChar = polarBearChar
        self.emptyCellChar = emptyCellChar
        self.trajectoryChar = 'x'
        self.actions = [(1,1), (1,3), (1,5), (1,7), (2,1)]
        pass
    def getDimension(self):
        return self.booleanRepresentation.shape

    #performs an action based on a state (x,y,isTerminal) tuple and returns the new state and the reward as (newState,reward) tuple
    #if action is not possible None is returned

    def performAction(self,currentState:tuple,action:tuple) ->tuple:
        if currentState[0] + action[0] >= self.booleanRepresentation.shape[0]:
            return None
        else:
            isTerminal = currentState[0] + action[0] == self.booleanRepresentation.shape[0]-1
            nextState = (currentState[0] + action[0], currentState[1] + action[1], isTerminal)
            reward = self.booleanRepresentation[currentState[0] + action[0],currentState[1] + action[1]] * (-1)
            return (nextState,reward)

    def getPossibleActionIndices(self,currentState:tuple) ->list:
        if currentState[0] + 2 <= self.booleanRepresentation.shape[0]-1:
            return np.arange(len(self.actions))
        elif currentState[0] + 1 <= self.booleanRepresentation.shape[0]-1:
            return np.array([0,1,2,3])
        else:
            return []


    def readFromFile(self,inputFile:str,replicateRows=True):
        with open(inputFile) as f:
            content = f.readlines()
            content = [element.strip("\n") for element in content]
            content = [splitWordIntoChars(element) for element in content]
            content_asNumpy  = np.array(content)
            self.booleanRepresentation = content_asNumpy == ord(self.polarBearChar)
            #replicate
            if replicateRows:
                nRows = self.booleanRepresentation.shape[0]
                nCols = self.booleanRepresentation.shape[1]
                #as 7 is the max x direction to go
                maxItemsPerRowNeeded = nRows*7
                repsNeeded = int(np.ceil(maxItemsPerRowNeeded/nCols))
                print(f"Replicating {repsNeeded} times")
                self.booleanRepresentation = np.tile(self.booleanRepresentation,repsNeeded)
                pass

    def writeTrajectoryToFile(self,trajectory,fileName):
        with open(fileName,"w") as f:
            trajectoryMatrix = self.__trajectoryToMatrix(trajectory)

            shape = self.booleanRepresentation.shape
            for nRow in range(shape[0]):
                for nCol in range(shape[1]):
                    if trajectoryMatrix[nRow][nCol] == 1:
                        f.write(self.trajectoryChar)
                    else:
                        if self.booleanRepresentation[nRow][nCol] == 1:
                            f.write(self.polarBearChar)
                        else:
                            f.write(self.emptyCellChar)


                f.write("\n")

    def visualizeTrajectory(self,trajectory):
        trajectoryMatrix = self.__trajectoryToMatrix(trajectory)

        shape = self.booleanRepresentation.shape
        for nRow in range(shape[0]):
            for nCol in range(shape[1]):
                if self.booleanRepresentation[nRow][nCol] == 1:
                    if trajectoryMatrix[nRow][nCol] == 1:
                        print(colored(self.polarBearChar, 'red'),end='')
                    else:
                        print(self.polarBearChar, end='')
                else:
                    if trajectoryMatrix[nRow][nCol] == 1:
                        print(colored(self.trajectoryChar, 'green'), end='')
                    else:
                        print(self.emptyCellChar, end='')
            print("\n")


    def printRepresentation(self):
        shape = self.booleanRepresentation.shape
        for nRow in range(shape[0]):
            for nCol in range(shape[1]):
                if self.booleanRepresentation[nRow][nCol] == 1:
                    print(self.polarBearChar, end='')
                else:
                    print(self.emptyCellChar, end='')
            print("\n")


    #returns a trajectory which is an array of tuples of the form (currentState,inputAction,newState,reward)
    def computeTrajectoryForOnlyOneAction(self,inputAction:tuple) -> int:
        currentState = (0,0,False)
        isTerminal = currentState[2]
        trajectory = []
        while not isTerminal:
            try:
                newState,reward = self.performAction(currentState,inputAction)
            except:
                print(f"Action {inputAction} not possible in current state {currentState}. Terminating...")
                return []
            isTerminal = newState[2]
            trajectory.append((currentState,inputAction,newState,reward))
            currentState = newState

        return trajectory

    def computeTotalRewardForTrajectory(self,trajectory):
        accumulatedReward = 0
        for currentState, inputAction, newState, reward in trajectory:
            accumulatedReward += reward
        return accumulatedReward


    def __trajectoryToMatrix(self,trajectory) -> np.array:
        matrix = np.zeros_like(self.booleanRepresentation,dtype=bool)
        for currentState,inputAction,newState,reward in trajectory:
            matrix[currentState[0],currentState[1]] = True
            matrix[newState[0],newState[1]] = True
        return matrix




