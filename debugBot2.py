import shipFile
from shipFile import Ship, getValidNeighbors, findDistanceBetween, findDistanceBetweenBot1, findDistanceBetweenBot4
import numpy as np
import random
import matplotlib.pyplot as plt
import math

# need to find binary search function for q values
qList = [0, 1]


def binarySearchQVals(low, high):
    if high - low >= 0.02:
        mid = (low + high) / 2
        qList.append(mid)
        binarySearchQVals(mid, high)
        binarySearchQVals(low, mid)
        print("Length of list is: " + str(len(qList)))


binarySearchQVals(0, 1)
qList = sorted(qList)

# find # of trials that should be performed for each q value based on confidence intervals
''''#
    Given to us by professor:
    pHat = s/n where s = # of successful trials and n = # of total trials
    p is in [phat - ε, phat + ε] with 95% confidence
    [pHat - 1.96sqrt((pHat(1-pH))/n), pHat + 1.96sqrt((pHat(1-pHat))/n)]
    Width of interval = 2*1.96*sqrt((pHat(1-pHat))/n) ≤ 2*1.96*sqrt(0.25/n)
    Number of trials greatest when q = 0.5
    n = (q(1-q))/((0.1/(2*1.96))^2)
    Solve for n when q = 0.5: [2*1.96*sqrt(0.25/n) = 0.1]
    n = (q(1-q))/((0.1/(2*1.96))^2)
    n = 384.16
    '''

numTrialsPerQVal = []
# set width of confidence interval
widthOfInterval = 0.1
for q in qList:
    if q == 0 or q == 1:
        n = (qList[1] * (1 - qList[1])) / ((widthOfInterval / (2 * 1.96)) ** 2)
    else:
        n = (q * (1 - q)) / ((widthOfInterval / (2 * 1.96)) ** 2)
    # need to floor value in case it's a float
    numTrialsPerQVal.append(math.floor(n))


def spreadFireBot4(arr, neighborsOfFire, size, q, fireCells, neighborsOfNeighborsFire, visited):
    for neighbor in neighborsOfFire:
        if arr[neighbor[0]][neighbor[1]][0] == 5:  # direct neighbor of a fire cell
            k = numFireNeighbors(getValidNeighbors(neighbor[0], neighbor[1], size), arr)
            prob = 1 - ((1 - q) ** k)
            rand = random.random()
            if rand < prob:  # the cell catches on fire
                arr[neighbor[0]][neighbor[1]][0] = 2
                neighborsOfFire.remove(neighbor)
                fireCells.append(neighbor)
                neighborsOfNewFireCell = getValidNeighbors(neighbor[0], neighbor[1], size)
                for newNeighbor in neighborsOfNewFireCell:
                    # if newNeighbor not in neighborsOfFire and arr[newNeighbor[0]][newNeighbor[1]][0] == 1:
                    if arr[newNeighbor[0]][newNeighbor[1]][0] == 4 or arr[newNeighbor[0]][newNeighbor[1]][0] == 1:
                        if arr[newNeighbor[0]][newNeighbor[1]][0] == 4:
                            neighborsOfNeighborsFire.remove(newNeighbor)
                        arr[newNeighbor[0]][newNeighbor[1]][0] = 5  # now cell is a direct neighbor of fire
                        neighborsOfFire.append(newNeighbor)
                        dist2FromFire = getValidOpenVal1(newNeighbor[0], newNeighbor[1], size, arr, visited)
                        for dist2 in dist2FromFire:
                            arr[dist2[0]][dist2[1]][0] = 4  # now cell is a neighbor of a neighbor on fire
                            neighborsOfNeighborsFire.add(dist2)



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


def getValidOpenVal1(row, col, size, arr, visited) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] == 1 and visited[valid[0]][valid[1]] == 0:
            validOpen.append(tuple(valid))
    return validOpen


winsHashtableBot4 = {}
for q in qList:
    winsHashtableBot4[q] = 0

for q in qList:
    numTrials = numTrialsPerQVal[qList.index(q)]
    for count in range(numTrials):
        print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 4")
        ship4 = Ship()
        size4 = ship4.size
        arr4 = ship4.arr
        bot4 = tuple(ship4.bot)
        button4 = tuple(ship4.button)
        visited = np.zeros((size4, size4))
        # make lists for tracking burning cells and neighbors of burning cells
        firstCellOnFire4 = tuple(ship4.firstCellOnFire)
        print("This is the button:")
        print(button4)
        print("This is the first cell on fire:")
        print(firstCellOnFire4)
        print("This is start of bot:")
        print(bot4)

        # if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win, so we can
        # stop simulation
        botToButton = findDistanceBetween(bot4[0], bot4[1], button4[0], button4[1], size4, arr4)
        fireToButton = findDistanceBetween(firstCellOnFire4[0], firstCellOnFire4[1], button4[0], button4[1], size4,
                                           arr4)
        if botToButton <= fireToButton:
            print("win: bot is closer")
            winsHashtableBot4[q] = winsHashtableBot4[q] + 1
            continue

        # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
        if q == 1 and botToButton > fireToButton:
            continue

        fireCells4 = [firstCellOnFire4]
        # distancesHashtable3 = ship3.distancesHashtable

        # mark the neighbors of the fire cells and the neighbors of the neighbors of the fire cells with weights
        neighborsOfFire4 = getValidOpenVal1(firstCellOnFire4[0], firstCellOnFire4[1], size4, arr4, visited)
        neighborsOfNeighborsFire = []
        for neighbor in neighborsOfFire4:
            arr4[neighbor[0]][neighbor[1]][0] = 5  # mark this neighbor as a neighbor of a fire cell
            listNeighbors = getValidOpenVal1(neighbor[0], neighbor[1], size4, arr4, visited)
            for neighborOfNeighbor in listNeighbors:
                if neighborOfNeighbor not in neighborsOfNeighborsFire and neighborOfNeighbor not in neighborsOfFire4:
                    arr4[neighborOfNeighbor[0]][neighborOfNeighbor[1]][0] = 4
                    neighborsOfNeighborsFire.append(neighborOfNeighbor)

        # mark cells with distance 1, 2, and 3 from the button with respective weights
        dist1FromButton = getValidOpenVal1(button4[0], button4[1], size4, arr4, visited)
        markedCells = [button4]  # keep track of cells already assigned a weight based on distance to button
        for dist1 in dist1FromButton:
            arr4[dist1[0]][dist1[1]][1] = 3
            markedCells.append(dist1)
            dist2FromButton = getValidOpenVal1(dist1[0], dist1[1], size4, arr4, visited)
            for dist2 in dist2FromButton:
                if dist2 not in markedCells:
                    arr4[dist2[0]][dist2[1]][1] = 2
                    markedCells.append(dist2)
                    dist3FromButton = getValidOpenVal1(dist2[0], dist2[1], size4, arr4, visited)
                    for dist3 in dist3FromButton:
                        if dist3 not in markedCells:
                            arr4[dist3[0]][dist3[1]][1] = 1

        while arr4[bot4[0]][bot4[1]][0] != 2 and arr4[button4[0]][button4[1]][0] != 2:
            visited[bot4[0], bot4[1]] = 1
            # check if button is surrounded by only closed and on fire cells
            buttonNeighbors = getValidOpen(button4[0], button4[1], size4, arr4, firstCellOnFire4)
            noOpenAroundButton = True
            for neighbor in buttonNeighbors:
                if arr4[neighbor[0]][neighbor[1]][0] != 0:
                    noOpenAroundButton = False
                    break
            if noOpenAroundButton:
                break

            validOpen = getValidOpenVal1(bot4[0], bot4[1], size4, arr4, visited)

            if validOpen:
                distsOpenToButton = []
                for neighbor in validOpen:
                    neighborToButton = findDistanceBetweenBot4(neighbor[0], neighbor[1], button4[0], button4[1], size4, arr4, q, visited)
                    if neighborToButton == -1:  # no path found, so set this val to inf
                        distsOpenToButton.append(float('inf'))
                    else:
                        distsOpenToButton.append(neighborToButton)

                smallestIndex = -1
                if distsOpenToButton:
                    smallest = float('inf')
                    count = 0
                    for item in distsOpenToButton:
                        if item < smallest:
                            smallestIndex = count
                            smallest = item
                        count = count + 1

                if smallestIndex != -1:
                    bot4 = validOpen[smallestIndex]
            else:
                break
            print("after moving:" + str(bot4))
            print(bot4)
            if bot4 == button4:  # bot2[0] == button2[0] and bot2[1] == button2[1]:
                print("win bc bot reached button")
                winsHashtableBot4[q] = winsHashtableBot4[q] + 1
                break
            spreadFireBot4(arr4, neighborsOfFire4, size4, q, fireCells4, neighborsOfNeighborsFire, visited)

print("bot 4 results:")
for item in winsHashtableBot4:
    index = list(winsHashtableBot4.keys()).index(item)
    print(item, winsHashtableBot4[item] / numTrialsPerQVal[index])

yVals4 = []
for item in winsHashtableBot4:
    index = list(winsHashtableBot4.keys()).index(item)
    yVals4.append(winsHashtableBot4[item] / numTrialsPerQVal[index])

plt.plot(qList, yVals4, label='Bot 4', color='c')
halfConfidence = widthOfInterval / 2
plt.fill_between(qList, [y - halfConfidence for y in yVals4], [y + halfConfidence for y in yVals4], color='c',
                 alpha=0.5, label='Confidence Interval Bot 4')
plt.title("Success Rates of Four Bots for q Values 0-1")
plt.xlabel("Q values")
plt.ylabel("Success Rate")
plt.legend(loc='upper right')
plt.show()
