from shipFile import Ship, getValidNeighbors

ship = Ship()
size = ship.get_size()
# make lists for tracking burning cells and neighbors of burning cells
firstCellOnFire = ship.get_firstCellOnFire()
fireCells = [[firstCellOnFire]]
neighborsOfFireCells = [getValidNeighbors(firstCellOnFire[0], firstCellOnFire[1], size)]

# set up list of q values
start = 0
qList = []
while start <= 1:
    qList.append(start)
    start = start + 0.05
print(qList)

def numFireNeighbors(neighbors, arr) -> int:
    count = 0
    for neighbor in neighbors:
        if arr[neighbor[0]][neighbor[1]][0] == 2:
            count = count + 1
    return count

# Bot 1
