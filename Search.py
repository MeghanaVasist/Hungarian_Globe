import heapq
import sys

#function to compute the hash of the dictionary which contains the states of the 30 tiles.
#appends all the coordinates in the order that is given in the dictionary.
def computeHash(initial):
    inputCoordinates = []
    for i in range(0, 30):
        index = str(initial[i][0])
        if len(index) == 1:
            index = "00" + index
        elif len(index) == 2:
            index = "0" + index
        indexLat = index
        index = str(initial[i][1])
        if len(index) == 1:
            index = "00" + index
        elif len(index) == 2:
            index = "0" + index
        indexLong = index
        inputCoordinates.append(indexLat + indexLong)
    hashValue = "".join(inputCoordinates)
    return hashValue

#function to unhash the hashed value of the dictionary
#returns the dictionary from the hash value.
def unhash(hashValue):
    unhashCoordinates = [0, 1]
    unhashed = {}
    unhashValue = [hashValue[i:i + 6] for i in range(0, 180, 6)]
    lat1 = tuple()
    for i in range(0, len(unhashValue)):
        lat = [unhashValue[i][j:j + 3] for j in range(0, 6, 3)]
        lat = tuple(lat)
        x = int(lat[0])
        unhashCoordinates[0] = x
        y = int(lat[1])
        unhashCoordinates[1] = y
        unhashed[i] = (tuple(unhashCoordinates))
    return unhashed

#computes the final path of the solution from the initial state to the goal state
def findPath(stateSet, goalStateHash):
    hashedPath = []
    finalPath = []
    while(goalStateHash != 0):
        hashedPath.append(goalStateHash)
        finalPath.append(stateSet[goalStateHash][1])
        goalStateHash = stateSet[goalStateHash][0]
    finalPath.reverse()
    print("Final path is: ")
    for i in range(1, len(finalPath)):
        print(finalPath[i])
    print("Final path length: ", len(finalPath)-1)

#rotates the globe on the equator clockwise by 1 shift.
def equatorRotateAntiClockwise(initial):
    for i in range(0, len(initial)):
        if initial[i][0] == 90:
            initial1 = list(initial[i])
            y = initial1[1]
            y = (y + 30) % 360
            initial1[1] = y
            initial[i] = tuple(initial1)
    return initial

#rotates the globe on the equator anticlockwise by 1 shift.
def equatorRotateClockwise(initial):
    for i in range(0, len(initial)):
        if initial[i][0] == 90:
            initial1 = list(initial[i])
            y = initial1[1]
            if (y == 0):
                y = 330
            else:
                y = y - 30
            initial1[1] = y
            initial[i] = tuple(initial1)
    return initial

#rotates the globe on the longitude 0-180 clockwise by 1 shift.
def longitude0180Clockwise(initial):
    for i in range(0, len(initial)):
        x = initial[i][0]
        initial1 = list(initial[i])
        if initial1[1] == 0:
            if x < 180:
                x = x + 30
                if (x == 180):
                    initial1[1] = 180
                initial1[0] = x
        elif initial1[1] == 180:
            x = x - 30
            if x == 0:
                initial1[1] = 0
            initial1[0] = x
        initial[i] = tuple(initial1)
    return initial

#rotates the globe on the longitude 0-180 anticlockwise by 1 shift.
def longitude0180AntiClockwise(initial):
    for i in range(0, len(initial)):
        x = initial[i][0]
        initial1 = list(initial[i])
        if initial1[1] == 0:
            if x > 0:
                x = x - 30
            elif x == 0:
                x = x + 30
                initial1[1] = 180
            initial1[0] = x
        elif initial1[1] == 180:
            if x < 180:
                x = x + 30
            elif x == 180:
                x = x - 30
                initial1[1] = 0
            initial1[0] = x
        initial[i] = tuple(initial1)
    return initial

#rotates the globe on the longitude 90-270 clockwise by 1 shift.
def longitude90270Clockwise(initial):  # upward
    for i in range(0, len(initial)):
        x = initial[i][0]
        initial1 = list(initial[i])
        if initial1[0] == 0 and initial1[1] == 0:
            initial1[0] = 30
            initial1[1] = 90
        elif initial1[0] == 180 and initial1[1] == 180:
            initial1[0] = 150
            initial1[1] = 270
        elif initial1[1] == 90:
            x = x + 30
            if x == 180:
                initial1[1] = 180
            initial1[0] = x
        elif initial1[1] == 270:
            x = x - 30
            if x == 0:
                initial1[1] = 0
            initial1[0] = x
        initial[i] = tuple(initial1)
    return initial

#rotates the globe on the longitude 90-270 anticlockwise by 1 shift.
def longitude90270AntiClockwise(initial):  # downward
    for i in range(0, len(initial)):
        x = initial[i][0]
        initial1 = list(initial[i])
        if initial1[0] == 0 and initial1[1] == 0:
            initial1[0] = 30
            initial1[1] = 270
        elif initial1[0] == 180 and initial1[1] == 180:
            initial1[0] = 150
            initial1[1] = 90
        elif initial1[1] == 90:
            x = x - 30
            if x == 0:
                initial1[1] = 0
            initial1[0] = x
        elif initial1[1] == 270:
            x = x + 30
            if x == 180:
                initial1[1] = 180
            initial1[0] = x
        initial[i] = tuple(initial1)
    return initial

#hard coded values of the ideal position of the goal state of the globe.
goalState = {
    (0, 0): 0,
    (30, 0): 1,
    (60, 0): 2,
    (90, 0): 3,
    (90, 30): 4,
    (90, 60): 5,
    (90, 90): 6,
    (90, 120): 7,
    (90, 150): 8,
    (90, 180): 9,
    (90, 210): 10,
    (90, 240): 11,
    (90, 270): 12,
    (90, 300): 13,
    (90, 330): 14,
    (150, 90): 15,
    (120, 90): 16,
    (60, 90): 17,
    (30, 90): 18,
    (30, 270): 19,
    (60, 270): 20,
    (120, 270): 21,
    (150, 270): 22,
    (180, 180): 23,
    (150, 180): 24,
    (120, 180): 25,
    (60, 180): 26,
    (30, 180): 27,
    (150, 0): 28,
    (120, 0): 29
}
equatorAxis = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
longitude0180Axis = [0, 1, 2, 3, 29, 28, 23, 24, 25, 9, 26, 27]
longitude90270Axis = [0, 18, 17, 6, 16, 15, 23, 22, 21, 12, 20, 19]

#determining the heuristic: sum/10 for the current state.
def heuristic(initialState, targetState):
    current = {}
    target = {}
    h = []
    for i in range(0, len(initialState)):
        current[initialState[i]] = goalState[initialState[i]]
        target[targetState[i]] = goalState[targetState[i]]
    currentInverse = dict([[v, k] for k, v in current.items()])
    targetInverse = dict([[v, k] for k, v in target.items()])
    currentAxis = []
    targetAxis = []
    for (x, y) in zip(currentInverse.values(), targetInverse.values()):
        if current[x] != target[y]:
            currentStateIndex = current[x]
            targetStateIndex = target[y]
            if currentStateIndex == 3 or currentStateIndex == 9:
                currentAxis.append(equatorAxis)
                currentAxis.append(longitude0180Axis)
            elif currentStateIndex == 6 or currentStateIndex == 12:
                currentAxis.append(equatorAxis)
                currentAxis.append(longitude90270Axis)
            elif currentStateIndex == 0 or currentStateIndex == 23:
                currentAxis.append(longitude90270Axis)
                currentAxis.append(longitude0180Axis)
            elif currentStateIndex in equatorAxis:
                currentAxis.append(equatorAxis)
            elif currentStateIndex in longitude0180Axis:
                currentAxis.append(longitude0180Axis)
            elif currentStateIndex in longitude90270Axis:
                currentAxis.append(longitude90270Axis)
            if targetStateIndex == 3 or targetStateIndex == 9:
                targetAxis.append(equatorAxis)
                targetAxis.append(longitude0180Axis)
            elif targetStateIndex == 6 or targetStateIndex == 12:
                targetAxis.append(equatorAxis)
                targetAxis.append(longitude90270Axis)
            elif targetStateIndex == 0 or targetStateIndex == 23:
                targetAxis.append(longitude90270Axis)
                targetAxis.append(longitude0180Axis)
            elif targetStateIndex in equatorAxis:
                targetAxis.append(equatorAxis)
            elif targetStateIndex in longitude0180Axis:
                targetAxis.append(longitude0180Axis)
            elif targetStateIndex in longitude90270Axis:
                targetAxis.append(longitude90270Axis)
            hIndex = []
            for tAxis in targetAxis:
                for cAxis in currentAxis:
                    if cAxis == tAxis:
                        cIndex = cAxis.index(currentStateIndex)
                        tIndex = tAxis.index(targetStateIndex)
                        heur = abs(cIndex - tIndex)
                        if heur > 6:
                            heur = 12 - heur
                        hIndex.append(heur)
                    else:
                        if cAxis == equatorAxis:
                            if tAxis == longitude0180Axis:
                                intersectIndex = cAxis.index(3)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(3)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex3 = dist1 + dist2
                                hIndex.append(distIndex3)
                                intersectIndex = cAxis.index(9)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(9)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex9 = dist1 + dist2
                                hIndex.append(distIndex9)
                            if tAxis == longitude90270Axis:
                                intersectIndex = cAxis.index(6)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(6)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex6 = dist1 + dist2
                                hIndex.append(distIndex6)
                                intersectIndex = cAxis.index(12)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(12)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex12 = dist1 + dist2
                                hIndex.append(distIndex12)
                        if cAxis == longitude0180Axis:
                            if tAxis == equatorAxis:
                                intersectIndex = cAxis.index(3)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(3)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex3 = dist1 + dist2
                                hIndex.append(distIndex3)
                                intersectIndex = cAxis.index(9)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(9)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex9 = dist1 + dist2
                                hIndex.append(distIndex9)
                            if tAxis == longitude90270Axis:
                                intersectIndex = cAxis.index(0)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(0)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex0 = dist1 + dist2
                                hIndex.append(distIndex0)
                                intersectIndex = cAxis.index(23)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(23)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex23 = dist1 + dist2
                                hIndex.append(distIndex23)
                        if cAxis == longitude90270Axis:
                            if tAxis == equatorAxis:
                                intersectIndex = cAxis.index(6)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(6)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex6 = dist1 + dist2
                                hIndex.append(distIndex6)
                                intersectIndex = cAxis.index(12)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(12)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex12 = dist1 + dist2
                                hIndex.append(distIndex12)
                            if tAxis == longitude0180Axis:
                                intersectIndex = cAxis.index(0)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(0)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex0 = dist1 + dist2
                                hIndex.append(distIndex0)
                                intersectIndex = cAxis.index(23)
                                cIndex = cAxis.index(currentStateIndex)
                                dist1 = abs(cIndex - intersectIndex)
                                if dist1 > 6:
                                    dist1 = 12 - dist1
                                intersectIndex = tAxis.index(23)
                                tIndex = tAxis.index(targetStateIndex)
                                dist2 = abs(intersectIndex - tIndex)
                                if dist2 > 6:
                                    dist2 = 12 - dist2
                                distIndex23 = dist1 + dist2
                                hIndex.append(distIndex23)
            h.append(min(hIndex))
            hIndex.clear()
        currentAxis.clear()
        targetAxis.clear()
    finalHeuristic = 0
    for i in range(0, len(h)):
        finalHeuristic = finalHeuristic + h[i]
    return finalHeuristic/15

#Breadth First search algorithm.
def bfs(initial, target):
    queues = []
    hashTarget = computeHash(target)
    stateSet = {}
    stateSet[computeHash(initial)] = (0, "0")
    queues.append(initial)
    visited = set()
    visited.add(str(computeHash(initial)))
    i = 0
    flag = 0
    rotations = []
    rotations.append(equatorRotateClockwise)
    rotations.append(equatorRotateAntiClockwise)
    rotations.append(longitude0180Clockwise)
    rotations.append(longitude0180AntiClockwise)
    rotations.append(longitude90270Clockwise)
    rotations.append(longitude90270AntiClockwise)
    actions = []
    actions.append("Equator Rotate Clockwise")
    actions.append("Equator Rotate Anti Clockwise")
    actions.append("Longitude 0-180 Rotate Upward")
    actions.append("Longitude 0-180 Rotate Downward")
    actions.append("Longitude 90-270 Rotate Upward")
    actions.append("Longitude 90-270 Rotate Downward")
    queuesLength = []
    numberOfStatesExpanded = 0
    while flag == 0:
        for x in queues:
            numberOfStatesExpanded = numberOfStatesExpanded + 1
            for (rot, act) in zip(rotations, actions):
                rotState = rot(x.copy())
                i = i + 1
                hashRot = computeHash(rotState)
                if str(hashRot) not in visited:
                    visited.add(str(hashRot))
                    queues.append(rotState)
                    queuesLength.append(len(queues))
                    stateSet[hashRot] = (computeHash(x.copy()), act)
                if (hashRot == hashTarget):
                    findPath(stateSet, hashRot)
                    print("Number of states expanded: ", numberOfStatesExpanded)
                    print("Maximum size of the queue during the search: ", max(queuesLength))
                    flag = 1
                    return
            queues = queues[1:]

#A star search implementation.
def aStar(initial, target):
    heuristicQueue = []
    hashTarget = computeHash(target)
    stateSet = {}
    levelSet = {}
    hashInitial = computeHash(initial)
    stateSet[hashInitial] = (0, 0)
    levelSet[hashInitial] = 0
    heuristicQueue.append((-1, str(hashInitial)))
    visited = set()
    visited.add(str(hashInitial))
    rotations = []
    rotations.append(equatorRotateClockwise)
    rotations.append(equatorRotateAntiClockwise)
    rotations.append(longitude0180Clockwise)
    rotations.append(longitude0180AntiClockwise)
    rotations.append(longitude90270Clockwise)
    rotations.append(longitude90270AntiClockwise)
    actions = []
    actions.append("Equator Rotate Clockwise")
    actions.append("Equator Rotate Anti Clockwise")
    actions.append("Longitude 0-180 Rotate Upward")
    actions.append("Longitude 0-180 Rotate Downward")
    actions.append("Longitude 90-270 Rotate Upward")
    actions.append("Longitude 90-270 Rotate Downward")
    level = 0
    flag = 0
    xState = {}
    queueLength = []
    numberOfStatesExpanded = 0
    while flag == 0:
        xState = heuristicQueue[0][1]
        xState = unhash(xState)
        numberOfStatesExpanded = numberOfStatesExpanded + 1
        for (rot, act) in zip(rotations, actions):
            rotState = rot(xState.copy())
            hashRot = computeHash(rotState)
            rotHeuristic = heuristic(rotState, target)
            if str(hashRot) not in visited:
                visited.add(str(hashRot))
                stateSet[hashRot] = (computeHash(xState), act)
                levelSet[hashRot] = levelSet[stateSet[hashRot][0]] + 1
                level = levelSet[hashRot]
                heuristicQueue.append((rotHeuristic+level, str(hashRot)))   #adding the level to the heuristic value so that sibling is selected over the children for the same value of heuristic.
                queueLength.append(len(heuristicQueue))
            if hashTarget == hashRot:
                flag = 1
                findPath(stateSet, hashRot)
                print("Number of states expanded: ", numberOfStatesExpanded)
                print("Maximum size of the queue during the search: ", max(queueLength))
                return
        heuristicQueue.pop(0)
        heapq.heapify(heuristicQueue)

def main():
    pathFile = open(str(sys.argv[2]), "r")
    path = pathFile.readlines()
    i = 0
    initial = {}
    for x in path[1:-1]:
        initial[i] = x
        i = i + 1
    i = 0
    j = len(initial)
    for i in range(0, len(initial)):
        initial[i] = initial[i].replace('Tile(', '')[:-2]
    initialState = {}
    targetState = {}

    #extracting the coordinate values from the file.
    for i in range(0, len(initial)):
        temp1 = initial[i].split(',', 1)
        temp2 = temp1[1].split(' ', 2)
        initialState[i] = temp2[1][:-1]
        initialState[i] = tuple(int(state) for state in initialState[i].strip("()").split(","))
        targetState[i] = temp2[2].replace('Exact', '')
        targetState[i] = tuple(int(state) for state in targetState[i].strip("()").split(","))
    if(sys.argv[1] == "BFS"):
        bfs(initialState, targetState)
    elif(sys.argv[1] == "AStar"):
        aStar(initialState, targetState)
    elif(sys.argv[1] == "RBFS"):
        print("RBFS not implemented")

if __name__ == '__main__':
    main()




