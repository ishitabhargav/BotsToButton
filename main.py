import numpy as np

# rows, cols, elements = (5, 5, 2)
# arr = [[[0 for _ in range(elements)] for _ in range(cols)] for _ in range(rows)]
size = 5

arr = np.zeros((size, size, 2))

# arr[4][3][1] = 1

print(arr)

"""
for row in arr:
    for element in row:
        element = [2, 5]
        print(element)
print ('h')

for row in arr:
    for element in row:
        print(element)
"""

# open first cell at random
randRow = np.random.randint(1, size - 1)
randCol = np.random.randint(1, size - 1)

arr[randRow][randCol][0] = 1  # open first cell
closedNeighbors = []
openCells = [[randRow, randCol]]
print("Open Cells:")
print(openCells)
print()

def getValidNeighbors(row, col) -> list[[int, int]]:  # neighbors that are inbounds
    validNeighbors = []
    if row + 1 < size:
        validNeighbors.append([row + 1, col])
    if col + 1 < size:
        validNeighbors.append([row, col + 1])
    if row - 1 >= 0:
        validNeighbors.append([row - 1, col])
    if col - 1 >= 0:
        validNeighbors.append([row, col - 1])
    return validNeighbors


def numOpenNeighbors(validNeighbors) -> int:
    count = 0
    for neighbor in validNeighbors:  # count the number of open neighbors. if more than 1, we should remove this neighbor from the closed list
        if arr[neighbor[0]][neighbor[1]][0] == 1:
            count = count + 1
    return count

def numFireNeighbors(neighbors) -> int:
    count = 0
    for neighbor in neighbors:  # count the number of open neighbors. if more than 1, we should remove this neighbor from the closed list
        if arr[neighbor[0]][neighbor[1]][0] == 2:
            count = count + 1
    return count


def addNeighbors(row, col):  # adding inbound, closed, and not in closedNeighbors list neighbors to closedNeighbors
    validNeighbors = getValidNeighbors(row, col)
    for neighbor in validNeighbors:
        if arr[neighbor[0]][neighbor[1]][0] == 0 and neighbor not in closedNeighbors and numOpenNeighbors(
                getValidNeighbors(neighbor[0], neighbor[1])) == 1:
            closedNeighbors.append(neighbor)


addNeighbors(randRow, randCol)

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
    validNeighbors = getValidNeighbors(rowToOpen, colToOpen)
    for neighbor in validNeighbors:
        if arr[neighbor[0]][neighbor[1]][0] == 0:  # it's a closed neighbor
            neighborsOfClosed = getValidNeighbors(neighbor[0], neighbor[1])
            if numOpenNeighbors(neighborsOfClosed) > 1 and neighbor in closedNeighbors:
                closedNeighbors.remove(neighbor)
    # 3. add the closed neighbors of neighborToOpen
    addNeighbors(rowToOpen, colToOpen)
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
    if numOpenNeighbors(getValidNeighbors(cell[0], cell[1])) == 1:
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
    validNeighbors = getValidNeighbors(deadEnd[0], deadEnd[1])
    for neighbor in validNeighbors: # can change to x, y
        if arr[neighbor[0]][neighbor[1]][0] == 0:
            deadEndsClosedNeighbors.append(neighbor)
    randCell = np.random.randint(0, len(deadEndsClosedNeighbors))
    deadEndNeighbor = deadEndsClosedNeighbors.pop(randCell)
    arr[deadEndNeighbor[0]][deadEndNeighbor[1]][0] = 1
    for deadEnd in deadEnds:
        if numOpenNeighbors(getValidNeighbors(deadEnd[0], deadEnd[1])) != 1:
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

# pick 3 different locations for fire, bot, and button
indexFirstCellOnFire = np.random.randint(0, len(openCells))
firstCellOnFire = openCells.pop(indexFirstCellOnFire)
arr[firstCellOnFire[0]][firstCellOnFire[1]][0] = 2 # this cell is on fire
indexBot = np.random.randint(0, len(openCells))
bot = openCells.pop(indexBot)
indexButton = np.random.randint(0, len(openCells))
button = openCells.pop(indexButton)

# add the cells back into the openCells list
openCells.append(firstCellOnFire)
openCells.append(bot)
openCells.append(button)

# make lists for tracking burning cells and neighbors of burning cells
fireCells = [[firstCellOnFire]]
neighborsOfFireCells = [getValidNeighbors(firstCellOnFire[0], firstCellOnFire[1])]

# set up fire spreading parameters
q = 0.5

#while arr[bot[0]][bot[1]][0] != 2 and arr[button[0]][button[1]][0] != 2:


for row in arr:
    for col in row:
        if col[0] == 1:  # it's open
            print("1", end="")
        else:
            print("O", end="")
    print("\n")
