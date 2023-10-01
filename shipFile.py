import numpy as np
from collections import deque


def getValidNeighbors(row, col, size) -> list[(int, int)]:  # neighbors that are inbounds
    validNeighbors = []
    if row + 1 < size:
        validNeighbors.append((row + 1, col))
    if col + 1 < size:
        validNeighbors.append((row, col + 1))
    if row - 1 >= 0:
        validNeighbors.append((row - 1, col))
    if col - 1 >= 0:
        validNeighbors.append((row, col - 1))
    return validNeighbors


def numOpenNeighbors(validNeighbors, arr) -> int:
    count = 0
    for neighbor in validNeighbors:  # count the number of open neighbors. if more than 1, we should remove this neighbor from the closed list
        if arr[neighbor[0]][neighbor[1]][0] == 1:
            count = count + 1
    return count


def addNeighbors(row, col, arr, closedNeighbors,
                 size):  # adding inbound, closed, and not in closedNeighbors list neighbors to closedNeighbors
    validNeighbors = getValidNeighbors(row, col, size)
    for neighbor in validNeighbors:
        if arr[neighbor[0]][neighbor[1]][0] == 0 and neighbor not in closedNeighbors and numOpenNeighbors(
                getValidNeighbors(neighbor[0], neighbor[1], size), arr) == 1:
            closedNeighbors.append(neighbor)


def findDistanceBetween(x1, y1, x2, y2, size, arr) -> int:
    queue = deque([(x1, y1)])
    arr[x1][y1][1] = 1
    distanceFromX1Y1 = {(x1, y1): 0}
    visited = np.zeros((size, size))
    visited[x1][y1] = 1
    while queue:
        x, y = queue.popleft()
        for next_x, next_y in getValidNeighbors(x, y, size):
            if visited[next_x][next_y] != 1 and arr[next_x][next_y][0] == 1:
                if next_x == x2 and next_y == y2:
                    return distanceFromX1Y1[(x, y)] + 1
                queue.append((next_x, next_y))
                visited[next_x][next_y] = 1
                distanceFromX1Y1[(next_x, next_y)] = distanceFromX1Y1[(x, y)] + 1
    return -1 # something went wrong: never got to (x2, y2)


class Ship:
    size = 5
    arr = np.zeros((size, size, 2))
    print(arr)
    # open first cell at random
    randRow = np.random.randint(1, size - 1)
    randCol = np.random.randint(1, size - 1)

    arr[randRow][randCol][0] = 1  # open first cell
    closedNeighbors = []
    openCells = [[randRow, randCol]]
    print("Open Cells:")
    print(openCells)
    print()
    addNeighbors(randRow, randCol, arr, closedNeighbors, size)

    for row in arr:
        for col in row:
            if col[0] == 1:  # it's open
                print("1", end="")
            else:
                print("O", end="")
        print("\n")
    print("\n")

    while closedNeighbors:  # choose a closed neighbor at random to open, from list of closed cells with one open neighbor
        # 1. pick a closed neighbor and open it at random
        sizeClosedNeighbors = len(closedNeighbors)
        rand = np.random.randint(0, sizeClosedNeighbors)
        neighborToOpen = closedNeighbors.pop(rand)
        rowToOpen = neighborToOpen[0]
        colToOpen = neighborToOpen[1]
        arr[rowToOpen][colToOpen][0] = 1
        openCells.append([rowToOpen, colToOpen])
        # 2. remove existing neighbors in closedNeighbors that now have 2 or more open neighbors
        validNeighbors = getValidNeighbors(rowToOpen, colToOpen, size)
        for neighbor in validNeighbors:
            if arr[neighbor[0]][neighbor[1]][0] == 0:  # it's a closed neighbor
                neighborsOfClosed = getValidNeighbors(neighbor[0], neighbor[1], size)
                if numOpenNeighbors(neighborsOfClosed, arr) > 1 and neighbor in closedNeighbors:
                    closedNeighbors.remove(neighbor)
        # 3. add the closed neighbors of neighborToOpen
        addNeighbors(rowToOpen, colToOpen, arr, closedNeighbors, size)
        for row in arr:
            for col in row:
                if col[0] == 1:  # it's open
                    print("1", end="")
                else:
                    print("O", end="")
            print("\n")
        print("Open Cells:")
        print(openCells)
        print("\n")

    deadEnds = []
    for cell in openCells:
        if numOpenNeighbors(getValidNeighbors(cell[0], cell[1], size), arr) == 1:
            deadEnds.append(cell)

    print("Dead Ends:")
    print(deadEnds)
    print("\n")
    origNumDeadEnds = len(deadEnds)
    print("Now starting with dead ends.\n")
    while len(deadEnds) > 0.50 * origNumDeadEnds:
        randCell = np.random.randint(0, len(deadEnds))
        deadEnd = deadEnds.pop(randCell)
        deadEndsClosedNeighbors = []
        validNeighbors = getValidNeighbors(deadEnd[0], deadEnd[1], size)
        for neighbor in validNeighbors:  # can change to x, y
            if arr[neighbor[0]][neighbor[1]][0] == 0:
                deadEndsClosedNeighbors.append(neighbor)
        randCell = np.random.randint(0, len(deadEndsClosedNeighbors))
        deadEndNeighbor = deadEndsClosedNeighbors.pop(randCell)
        arr[deadEndNeighbor[0]][deadEndNeighbor[1]][0] = 1
        for deadEnd in deadEnds:
            if numOpenNeighbors(getValidNeighbors(deadEnd[0], deadEnd[1], size), arr) != 1:
                deadEnds.remove(deadEnd)
        openCells.append(deadEndNeighbor)
        for row in arr:
            for col in row:
                if col[0] == 1:  # it's open
                    print("1", end="")
                else:
                    print("O", end="")
            print("\n")
        print("Dead ends now:")
        print(deadEnds)
        print("\n")

    print("End of Dead Ends\n")
    distancesHashtable = {}

    for x1 in range(size):
        for y1 in range(size):
            for x2 in range(x1, size):
                for y2 in range(y1, size):
                    if arr[x1][y1][0] == 1 and arr[x2][y2][0] == 1:  # make sure both cells are open
                        if x1 == x2 and y1 == y2:
                            distancesHashtable[((x1, y1), (x2, y2))] = 0  # dist to itself is 0
                            print("distance from (" + str(x1) + ", " + str(y1) + ") to (" + str(x2) + ", " + str(y2) +
                                  ") is 0")
                        else:
                            distancesHashtable[((x1, y1), (x2, y2))] = findDistanceBetween(x1, y1, x2, y2, size, arr)
                            print("distance from (" + str(x1) + ", " + str(y1) + ") to (" + str(x2) + ", " + str(y2) +
                                  ") is " + str(distancesHashtable[((x1, y1), (x2, y2))]))

    # pick 3 different locations for fire, bot, and button
    indexFirstCellOnFire = np.random.randint(0, len(openCells))
    firstCellOnFire = openCells.pop(indexFirstCellOnFire)
    arr[firstCellOnFire[0]][firstCellOnFire[1]][0] = 2  # this cell is on fire
    indexBot = np.random.randint(0, len(openCells))
    bot = openCells.pop(indexBot)
    indexButton = np.random.randint(0, len(openCells))
    button = openCells.pop(indexButton)

    # add the cells back into the openCells list
    openCells.append(firstCellOnFire)
    openCells.append(bot)
    openCells.append(button)

    # while arr[bot[0]][bot[1]][0] != 2 and arr[button[0]][button[1]][0] != 2:

    for row in arr:
        for col in row:
            if col[0] == 1:  # it's open
                print("1", end="")
            elif col[0] == 0:  # it's closed
                print("O", end="")
            else:  # it's on fire
                print("2", end="")
        print("\n")

    def get_firstCellOnFire(self):
        return self.firstCellOnFire

    def get_bot(self):
        return self.bot

    def get_button(self):
        return self.button

    def get_validNeighbors(self):
        return self.validNeighbors

    def get_size(self):
        return self.size
