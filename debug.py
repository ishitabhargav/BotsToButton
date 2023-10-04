from shipFile import Ship, getValidNeighbors
import numpy as np
import random

# set up list of q values
qList = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]


def spreadFire(arr, neighborsOfFire, size, q, fireCells):
    for neighbor in neighborsOfFire:
        if arr[neighbor[0]][neighbor[1]][0] == 1:
            k = numFireNeighbors(getValidNeighbors(neighbor[0], neighbor[1], size), arr)
            prob = 1 - ((1 - q) ** k)
            rand = random.random() #np.random.rand(0, 1)
            if rand < prob:  # the cell catches on fire
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
#for q in qList:
    #for count in range(10):
        #print("Q value and count value are as follows: " + str(q) + " " + str(count))
q = 0.95
ship = Ship()
size = ship.size
arr = ship.arr
# make lists for tracking burning cells and neighbors of burning cells
firstCellOnFire = tuple(ship.firstCellOnFire)
fireCells = [firstCellOnFire]
neighborsOfFire = getValidNeighbors(firstCellOnFire[0], firstCellOnFire[1], size)
for neighbor in neighborsOfFire:
    if arr[neighbor[0]][neighbor[1]][0] == 0:
        neighborsOfFire.remove(neighbor)

bot = tuple(ship.bot)
button = tuple(ship.button)
distancesHashtable = ship.distancesHashtable
print("This is the button:")
print(button)
print("This is the first cell on fire:")
print(firstCellOnFire)
print("This is start of bot: " + str(bot))
print(bot)

# if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win, so we can stop simulation
alreadyWon = False
if distancesHashtable[(bot, button)] <= distancesHashtable[(firstCellOnFire, button)]:
    print("win: bot is closer")
    alreadyWon = True
    winsHashtableBot1[q] = winsHashtableBot1[q] + 1
    #continue

# if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
#if q == 1 and distancesHashtable[(bot, button)] > distancesHashtable[(firstCellOnFire, button)]:
    #continue

minDistance = distancesHashtable[(bot, button)]

while arr[bot[0]][bot[1]][0] != 2 and arr[button[0]][button[1]][0] != 2 and not alreadyWon:
    # check if button is surrounded by only closed and on fire cells
    for item in fireCells:
        print("fire cells" + str(item), end="")
    print("\n")
    buttonNeighbors = getValidOpen(button[0], button[1], size, arr, firstCellOnFire)
    noOpenAroundButton = True
    for neighbor in buttonNeighbors:
        if arr[neighbor[0]][neighbor[1]][0] == 1:
            noOpenAroundButton = False
            break
    if noOpenAroundButton:
        break

    validOpen = getValidOpen(bot[0], bot[1], size, arr, firstCellOnFire)
    #print(bot)

    nextCell = bot
    for neighbor in validOpen:
        if distancesHashtable[(neighbor, button)] < minDistance:
            print("This is the current min distance " + str(minDistance))
            minDistance = distancesHashtable[(neighbor, button)]
            nextCell = neighbor

    if nextCell == bot:
        break
    bot = nextCell
    # print("This is the (new) bot location")
    print(bot)

    if bot[0] == button[0] and bot[1] == button[1]:  # bot == button: #
        print("win bc bot reached button")
        winsHashtableBot1[q] = winsHashtableBot1[q] + 1
        break
    spreadFire(arr, neighborsOfFire, size, q, fireCells)

for item in winsHashtableBot1:
    print(item, winsHashtableBot1[item])
