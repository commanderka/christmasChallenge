
from iceWorld import IceWorld
from solver import QLearningSolver
if __name__ == '__main__':
    inputFile = "input/input.txt"
    myIceWorld = IceWorld()
    myIceWorld.readFromFile(inputFile)
    #trajectory = myIceWorld.computeTrajectoryForOnlyOneAction((2,1))
    #myIceWorld.visualizeTrajectory(trajectory)
    #totalReward = myIceWorld.computeTotalRewardForTrajectory(trajectory)
    #nPolarBearsHit = -totalReward
    #polarBearsPerStep = nPolarBearsHit/len(trajectory)
    #print(f"Oh no. Hit {nPolarBearsHit} polar bears while doing {len(trajectory)} steps. This means an average hit rate per step of {polarBearsPerStep}!")
    mySolver = QLearningSolver(myIceWorld)
    mySolver.solve()
    optimalTrajectory = mySolver.getOptimalTrajectory()
    print(f"Optimal trajectory: {optimalTrajectory}")
    myIceWorld.visualizeTrajectory(optimalTrajectory)


