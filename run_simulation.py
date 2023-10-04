from shipFile import Ship, getValidNeighbors
import numpy as np


# set up list of q values
qList = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

"""
qList = []
start = 0
while start <= 1:
    qList.append(start)
    start = start + 0.05

for item in qList:
    print(item)
print("done")
"""


def spreadFire(arr, neighborsOfFire, size, q, fireCells):
    for neighbor in neighborsOfFire:
        if arr[neighbor[0]][neighbor[1]][0] == 1:
            k = numFireNeighbors(getValidNeighbors(neighbor[0], neighbor[1], size), arr)
            prob = 1 - (1 - q) ** k
            rand = np.random.randint(0, 1)
            if rand >= prob:  # the cell catches on fire
                arr[neighbor[0]][neighbor[1]][0] = 2
                neighborsOfFire.remove(neighbor)
                fireCells.append(neighbor)
                neighborsOfNewFireCell = getValidNeighbors(neighbor[0], neighbor[1], size)
                for newNeighbor in neighborsOfNewFireCell:
                    if newNeighbor not in neighborsOfFire and arr[newNeighbor[0]][newNeighbor[1]][0] == 1:
                        neighborsOfFire.append(newNeighbor)

def numFireNeighbors(neighbors, arr) -> int:
    count = 0
    for neighbor in neighbors:
        if arr[neighbor[0]][neighbor[1]][0] == 2:
            count = count + 1
    return count

def getValidOpen(row, col, size, arr, firstCellOnFire) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] != 0 and valid != firstCellOnFire:
            validOpen.append(tuple(valid))
    return validOpen


winsHashtableBot1 = {}
winsHashtableBot2 = {}
winsHashtableBot3 = {}
winsHashtableBot4 = {}
for q in qList:
    winsHashtableBot1[q] = 0
    winsHashtableBot2[q] = 0
    winsHashtableBot3[q] = 0
    winsHashtableBot4[q] = 0

# Bot 1
