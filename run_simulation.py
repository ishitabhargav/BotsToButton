import shipFile
from shipFile import Ship, getValidNeighbors, findDistanceBetween
import numpy as np
import random
import matplotlib.pyplot as plt
import math

# set up list of q values
# no need to hardcode q values
# qList = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

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
widthOfInterval = 0.15
for q in qList:
    if q == 0 or q == 1:
        n = (qList[1]*(1-qList[1]))/((widthOfInterval/(2*1.96))**2)
    else:
        n = (q*(1-q))/((widthOfInterval/(2*1.96))**2)
    # need to floor value in case it's a float
    numTrialsPerQVal.append(math.floor(n))


'''start = 0
while start <= 1:
    qList.append(start)
    start = start + 0.01'''

for item in qList:
    print(item)
print("length of list" + str(len(qList)))


def spreadFireBot1(arr, neighborsOfFire, size, q, fireCells):
    for neighbor in neighborsOfFire:
        if arr[neighbor[0]][neighbor[1]][0] == 1:
            k = numFireNeighbors(getValidNeighbors(neighbor[0], neighbor[1], size), arr)
            prob = 1 - ((1 - q) ** k)
            rand = random.random()  # np.random.rand(0, 1)
            if rand < prob:  # the cell catches on fire
                arr[neighbor[0]][neighbor[1]][0] = 2
                neighborsOfFire.remove(neighbor)
                fireCells.append(neighbor)
                neighborsOfNewFireCell = getValidNeighbors(neighbor[0], neighbor[1], size)
                for newNeighbor in neighborsOfNewFireCell:
                    if newNeighbor not in neighborsOfFire and arr[newNeighbor[0]][newNeighbor[1]][0] == 1:
                        neighborsOfFire.append(newNeighbor)


def spreadFireBot3(arr, neighborsOfFire, size, q, fireCells):
    for neighbor in neighborsOfFire:
        if arr[neighbor[0]][neighbor[1]][0] == 3:
            k = numFireNeighbors(getValidNeighbors(neighbor[0], neighbor[1], size), arr)
            prob = 1 - ((1 - q) ** k)
            rand = random.random()  # np.random.rand(0, 1)
            if rand < prob:  # the cell catches on fire
                arr[neighbor[0]][neighbor[1]][0] = 2
                neighborsOfFire.remove(neighbor)
                fireCells.append(neighbor)
                neighborsOfNewFireCell = getValidNeighbors(neighbor[0], neighbor[1], size)
                for newNeighbor in neighborsOfNewFireCell:
                    if newNeighbor not in neighborsOfFire and arr[newNeighbor[0]][newNeighbor[1]][0] == 1:
                        arr[newNeighbor[0]][newNeighbor[1]][0] = 3
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


def getValidOpenVal1(row, col, size, arr, visited) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] == 1 and visited[valid[0]][valid[1]] == 0:
            validOpen.append(tuple(valid))
    return validOpen


def getValidOpenVal3(row, col, size, arr, visited) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] == 3 and visited[valid[0]][valid[1]] == 0:
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
for q in qList:
    index = qList.index(q)
    for count in range(numTrialsPerQVal[index]):
        print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 1")
        ship1 = Ship()
        size1 = ship1.size
        arr1 = ship1.arr
        # make lists for tracking burning cells and neighbors of burning cells
        firstCellOnFire1 = tuple(ship1.firstCellOnFire)
        fireCells1 = [firstCellOnFire1]
        neighborsOfFire1 = getValidNeighbors(firstCellOnFire1[0], firstCellOnFire1[1], size1)
        for neighbor in neighborsOfFire1:
            if arr1[neighbor[0]][neighbor[1]][0] == 0:
                neighborsOfFire1.remove(neighbor)

        bot1 = tuple(ship1.bot)
        button1 = tuple(ship1.button)
        #distancesHashtable1 = ship1.distancesHashtable
        print("This is the button:")
        print(button1)
        print("This is the first cell on fire:")
        print(firstCellOnFire1)
        print("This is start of bot:")
        print(bot1)

        # if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win, so we can stop simulation
        botToButton = findDistanceBetween(bot1[0], bot1[1], button1[0], button1[1], size1, arr1)
        fireToButton = findDistanceBetween(firstCellOnFire1[0], firstCellOnFire1[1], button1[0], button1[1], size1, arr1)
        if botToButton <= fireToButton:
            print("win: bot is closer")
            winsHashtableBot1[q] = winsHashtableBot1[q] + 1
            continue

        # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
        if q == 1 and botToButton > fireToButton:
            continue

        minDistance1 = botToButton

        while arr1[bot1[0]][bot1[1]][0] != 2 and arr1[button1[0]][button1[1]][0] != 2:
            # check if button is surrounded by only closed and on fire cells
            buttonNeighbors = getValidOpen(button1[0], button1[1], size1, arr1, firstCellOnFire1)
            noOpenAroundButton = True
            for neighbor in buttonNeighbors:
                if arr1[neighbor[0]][neighbor[1]][0] == 1:
                    noOpenAroundButton = False
                    break
            if noOpenAroundButton:
                break

            validOpen = getValidOpen(bot1[0], bot1[1], size1, arr1, firstCellOnFire1)

            nextCell = bot1
            for neighbor in validOpen:
                neighborToButton = findDistanceBetween(neighbor[0], neighbor[1], button1[0], button1[1], size1, arr1)
                if neighborToButton < minDistance1:
                    print("This is the current min distance " + str(minDistance1))
                    minDistance1 = neighborToButton
                    nextCell = neighbor

            if nextCell == bot1:
                break
            bot1 = nextCell
            # print("This is the (new) bot location")
            print("after moving:" + str(bot1))

            if bot1[0] == button1[0] and bot1[1] == button1[1]:  # bot == button: #
                print("win bc bot reached button")
                winsHashtableBot1[q] = winsHashtableBot1[q] + 1
                break
            spreadFireBot1(arr1, neighborsOfFire1, size1, q, fireCells1)


# Bot 2
for q in qList:
    index = qList.index(q)
    for count in range(numTrialsPerQVal[index]):
        print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 2")
        ship2 = Ship()
        size2 = ship2.size
        arr2 = ship2.arr
        visited = np.zeros((size2, size2))
        # make lists for tracking burning cells and neighbors of burning cells
        firstCellOnFire2 = tuple(ship2.firstCellOnFire)
        fireCells2 = [firstCellOnFire2]
        # prevFireCells2 = fireCells2
        neighborsOfFire2 = getValidNeighbors(firstCellOnFire2[0], firstCellOnFire2[1], size2)
        for neighbor in neighborsOfFire2:
            if arr2[neighbor[0]][neighbor[1]][0] == 0:
                neighborsOfFire2.remove(neighbor)
        bot2 = tuple(ship2.bot)
        button2 = tuple(ship2.button)
        #distancesHashtable2 = ship2.distancesHashtable
        print("This is the button:")
        print(button2)
        print("This is the first cell on fire:")
        print(firstCellOnFire2)
        print("This is start of bot:")
        print(bot2)
        # if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win, so we can stop simulation
        botToButton = findDistanceBetween(bot2[0], bot2[1], button2[0], button2[1], size2, arr2)
        fireToButton = findDistanceBetween(firstCellOnFire2[0], firstCellOnFire2[1], button2[0], button2[1], size2, arr2)
        if botToButton <= fireToButton:
            print("win: bot is closer")
            winsHashtableBot2[q] = winsHashtableBot2[q] + 1
            continue

        # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
        if q == 1 and botToButton > fireToButton:
            continue

        while arr2[bot2[0]][bot2[1]][0] != 2 and arr2[button2[0]][button2[1]][0] != 2:
            visited[bot2[0], bot2[1]] = 1
            # check if button is surrounded by only closed and on fire cells
            buttonNeighbors = getValidOpen(button2[0], button2[1], size2, arr2, firstCellOnFire2)
            noOpenAroundButton = True
            for neighbor in buttonNeighbors:
                if arr2[neighbor[0]][neighbor[1]][0] == 1:
                    noOpenAroundButton = False
                    break
            if noOpenAroundButton:
                break

            validOpen = getValidOpenVal1(bot2[0], bot2[1], size2, arr2, visited)
            distsOpenToButton = []
            if not validOpen:
                break
            for neighbor in validOpen:
                neighborToButton = findDistanceBetween(neighbor[0], neighbor[1], button2[0], button2[1], size2, arr2)
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
                bot2 = validOpen[smallestIndex]
            else:
                break

            print("after moving:" + str(bot2))
            print(bot2)
            if bot2 == button2:  # bot2[0] == button2[0] and bot2[1] == button2[1]:
                print("win bc bot reached button")
                winsHashtableBot2[q] = winsHashtableBot2[q] + 1
                break
            spreadFireBot1(arr2, neighborsOfFire2, size2, q, fireCells2)

# Bot 3
for q in qList:
    index = qList.index(q)
    for count in range(numTrialsPerQVal[index]):
        print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 3")
        ship3 = Ship()
        size3 = ship3.size
        arr3 = ship3.arr
        visited = np.zeros((size3, size3))
        # make lists for tracking burning cells and neighbors of burning cells
        firstCellOnFire3 = tuple(ship3.firstCellOnFire)
        fireCells3 = [firstCellOnFire3]
        # prevFireCells3 = fireCells3
        neighborsOfFire3 = getValidNeighbors(firstCellOnFire3[0], firstCellOnFire3[1], size3)
        for neighbor in neighborsOfFire3:
            if arr3[neighbor[0]][neighbor[1]][0] == 0: # remove a closed cell from the list of neighbors of the first fire cell
                neighborsOfFire3.remove(neighbor)
            else:
                arr3[neighbor[0]][neighbor[1]][0] = 3 # mark this neighbor as a neighbor of a fire cell
        bot3 = tuple(ship3.bot)
        button3 = tuple(ship3.button)
        # distancesHashtable3 = ship3.distancesHashtable
        print("This is the button:")
        print(button3)
        print("This is the first cell on fire:")
        print(firstCellOnFire3)
        print("This is start of bot:")
        print(bot3)
        # if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win, so we can stop simulation
        botToButton = findDistanceBetween(bot3[0], bot3[1], button3[0], button3[1], size3, arr3)
        fireToButton = findDistanceBetween(firstCellOnFire3[0], firstCellOnFire3[1], button3[0], button3[1], size3, arr3)
        if botToButton <= fireToButton:
            print("win: bot is closer")
            winsHashtableBot3[q] = winsHashtableBot3[q] + 1
            continue

        # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
        if q == 1 and botToButton > fireToButton:
            continue

        while arr3[bot3[0]][bot3[1]][0] != 2 and arr3[button3[0]][button3[1]][0] != 2:
            visited[bot3[0], bot3[1]] = 1
            # check if button is surrounded by only closed and on fire cells
            buttonNeighbors = getValidOpen(button3[0], button3[1], size3, arr3, firstCellOnFire3)
            noOpenAroundButton = True
            for neighbor in buttonNeighbors:
                if arr3[neighbor[0]][neighbor[1]][0] == 1:
                    noOpenAroundButton = False
                    break
            if noOpenAroundButton:
                break

            validOpen = getValidOpenVal1(bot3[0], bot3[1], size3, arr3, visited)
            listToTraverse = []

            if validOpen:
                listToTraverse = validOpen
            else:
                listToTraverse = getValidOpenVal3(bot3[0], bot3[1], size3, arr3, visited)

            if listToTraverse:
                distsOpenToButton = []
                for neighbor in listToTraverse:
                    neighborToButton = findDistanceBetween(neighbor[0], neighbor[1], button3[0], button3[1], size3, arr3)
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
                    bot3 = listToTraverse[smallestIndex]
            else:
                break
            print("after moving:" + str(bot3))
            print(bot3)
            if bot3 == button3:  # bot2[0] == button2[0] and bot2[1] == button2[1]:
                print("win bc bot reached button")
                winsHashtableBot3[q] = winsHashtableBot3[q] + 1
                break
            spreadFireBot3(arr3, neighborsOfFire3, size3, q, fireCells3)

print("bot 1 results:")
for item in winsHashtableBot1:
    index = list(winsHashtableBot1.keys()).index(item)
    print(item, winsHashtableBot1[item]/numTrialsPerQVal[index])

print("bot 2 results:")
for item in winsHashtableBot2:
    index = list(winsHashtableBot2.keys()).index(item)
    print(item, winsHashtableBot2[item]/numTrialsPerQVal[index])

print("bot 3 results:")
for item in winsHashtableBot3:
    index = list(winsHashtableBot3.keys()).index(item)
    print(item, winsHashtableBot3[item]/numTrialsPerQVal[index])

yVals1 = []
for item in winsHashtableBot1:
    index = list(winsHashtableBot1.keys()).index(item)
    yVals1.append(winsHashtableBot1[item]/numTrialsPerQVal[index])

yVals2 = []
for item in winsHashtableBot2:
    index = list(winsHashtableBot2.keys()).index(item)
    yVals2.append(winsHashtableBot2[item]/numTrialsPerQVal[index])

yVals3 = []
for item in winsHashtableBot3:
    index = list(winsHashtableBot3.keys()).index(item)
    yVals3.append(winsHashtableBot3[item]/numTrialsPerQVal[index])

plt.plot(qList, yVals1, label='Bot 1')
plt.plot(qList, yVals2, label='Bot 2')
plt.plot(qList, yVals3, label='Bot 3')
plt.title("Success Rates of Four Bots for q Values 0-1")
plt.xlabel("Q values")
plt.ylabel("Success Rate")
plt.legend(loc='upper right')
plt.show()
