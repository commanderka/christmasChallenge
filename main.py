
from iceWorld import IceWorld
from solver import QLearningSolver
import os

if __name__ == '__main__':
    inputFile = "input/input.txt"
    outputDir ="output"
    outputTrajectoryFile = os.path.join(outputDir,"optimalTrajectory.txt")
    myIceWorld = IceWorld()
    myIceWorld.readFromFile(inputFile)
    print("Task 1/2")
    for currentAction in myIceWorld.actions:
        trajectory = myIceWorld.computeTrajectoryForOnlyOneAction(currentAction)
        #myIceWorld.visualizeTrajectory(trajectory)
        totalReward = myIceWorld.computeTotalRewardForTrajectory(trajectory)
        nPolarBearsHit = -totalReward
        if len(trajectory) > 0:
            polarBearsPerStep = nPolarBearsHit/len(trajectory)
            print(f"Oh no. Hit {nPolarBearsHit} polar bears while doing only action {currentAction} and {len(trajectory)} steps. This means an average hit rate per step of {polarBearsPerStep}!")
        else:
            print(f"No trajectory possible when only doing action {currentAction}")
    print("Task 3")
    mySolver = QLearningSolver(myIceWorld)
    optimalTrajectory,rewards = mySolver.solve()
    print(f"Number of polar bears hit with optimal trajectory: {-rewards}")
    print(f"Optimal trajectory: {optimalTrajectory}")
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    myIceWorld.visualizeTrajectory(optimalTrajectory)
    myIceWorld.writeTrajectoryToFile(optimalTrajectory,outputTrajectoryFile)




