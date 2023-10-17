from shipFile import Ship, getValidNeighbors, findDistanceBetween, findDistanceBetweenBot1, findDistanceBetweenBot4, \
    findDistanceBetweenBot3
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
'''
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


def spreadFireBot12(arr, neighborsOfFire, size, q, fireCells):
    newFireNeighbors = []
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
                        newFireNeighbors.append(newNeighbor)
    for neighbor in newFireNeighbors:
        if neighbor not in neighborsOfFire:
            neighborsOfFire.append(neighbor)


def spreadFireBot3(arr, neighborsOfFire, size, q, fireCells):
    newFireNeighbors = []
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
                        newFireNeighbors.append(newNeighbor)
    for neighbor in newFireNeighbors:
        if neighbor not in neighborsOfFire:
            neighborsOfFire.append(neighbor)


def spreadFireBot4(arr, neighborsOfFire, size, q, fireCells, neighborsOfNeighborsFire, cost1F, cost2F):
    newFireNeighbors = []
    newNeighborsOfFireNeighbors = []
    for neighbor in neighborsOfFire:
        if arr[neighbor[0]][neighbor[1]][0] == cost1F:  # direct neighbor of a fire cell
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
                    if arr[newNeighbor[0]][newNeighbor[1]][0] == cost2F or arr[newNeighbor[0]][newNeighbor[1]][0] == 1:
                        if arr[newNeighbor[0]][newNeighbor[1]][0] == cost2F:
                            neighborsOfNeighborsFire.remove(newNeighbor)
                        arr[newNeighbor[0]][newNeighbor[1]][0] = cost1F  # now cell is a direct neighbor of fire
                        newFireNeighbors.append(newNeighbor)
                        dist2FromFire = getValidOpenVal145(newNeighbor[0], newNeighbor[1], size, arr, cost1F,
                                                           cost2F)
                        for dist2 in dist2FromFire:
                            arr[dist2[0]][dist2[1]][0] = cost2F  # now cell is a neighbor of a neighbor on fire
                            newNeighborsOfFireNeighbors.append(dist2)
    for neighbor in newFireNeighbors:
        if neighbor not in neighborsOfFire:
            neighborsOfFire.append(neighbor)
    for neighbor in newNeighborsOfFireNeighbors:
        if neighbor not in neighborsOfNeighborsFire:
            neighborsOfNeighborsFire.append(neighbor)


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


def getValidOpenVal13(row, col, size, arr) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] == 1 or arr[valid[0]][valid[1]][0] == 3:
            validOpen.append(tuple(valid))
    return validOpen


def getValidOpenVal1(row, col, size, arr) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] == 1:  # and visited[valid[0]][valid[1]] == 0:
            validOpen.append(tuple(valid))
    return validOpen


def getValidOpenVal3(row, col, size, arr) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] == 3:  # and visited[valid[0]][valid[1]] == 0:
            validOpen.append(tuple(valid))
    return validOpen


def getValidOpenVal145(row, col, size, arr, cost1F, cost2F) -> list[(int, int)]:
    validNeighbors = getValidNeighbors(row, col, size)
    validOpen = []
    for valid in validNeighbors:
        if arr[valid[0]][valid[1]][0] == 1 or arr[valid[0]][valid[1]][0] == cost1F or arr[valid[0]][valid[1]][
            0] == cost2F:  # and visited[valid[0]][valid[1]] == 0:
            validOpen.append(tuple(valid))
    return validOpen


def cantReachFromNeighbors(distsOpenToButton) -> bool:
    b = True
    for item in distsOpenToButton:
        if item != -1:
            b = False
    return b


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
   numTrials = numTrialsPerQVal[qList.index(q)]
   for count in range(numTrials):
       print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 1")
       ship1 = Ship()
       size1 = ship1.size
       arr1 = ship1.arr
       firstCellOnFire1 = tuple(ship1.firstCellOnFire)
       bot1 = tuple(ship1.bot)
       button1 = tuple(ship1.button)


       print("This is the button:")
       print(button1)
       print("This is the first cell on fire:")
       print(firstCellOnFire1)
       print("This is start of bot:")
       print(bot1)


       # if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win,
       # so we can stop simulation
       botToButton = findDistanceBetweenBot1(bot1[0], bot1[1], button1[0], button1[1], size1, arr1, firstCellOnFire1)
       fireToButton = findDistanceBetweenBot1(firstCellOnFire1[0], firstCellOnFire1[1], button1[0], button1[1], size1,
                                              arr1, firstCellOnFire1)


       if botToButton == -1:
           continue


       if botToButton <= fireToButton:
           print("win: bot is closer")
           winsHashtableBot1[q] = winsHashtableBot1[q] + 1
           continue


       # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
       if q == 1 and botToButton > fireToButton:
           continue


       # make lists for tracking burning cells and neighbors of burning cells
       fireCells1 = [firstCellOnFire1]
       neighborsOfFire1 = getValidOpenVal1(firstCellOnFire1[0], firstCellOnFire1[1], size1, arr1)
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
               neighborToButton = findDistanceBetweenBot1(neighbor[0], neighbor[1], button1[0], button1[1], size1,
                                                          arr1, firstCellOnFire1)
               if neighborToButton == -1:  # it's the firstCellOnFire
                   neighborToButton = float('inf')
               if neighborToButton < minDistance1:
                   print("This is the current min distance " + str(minDistance1))
                   minDistance1 = neighborToButton
                   nextCell = neighbor


           if nextCell == bot1:
               break
           bot1 = nextCell
           print("after moving: Bot 1 " + str(bot1))

           if bot1[0] == button1[0] and bot1[1] == button1[1]:  # bot == button: #
               print("win bc bot reached button")
               winsHashtableBot1[q] = winsHashtableBot1[q] + 1
               break
           spreadFireBot12(arr1, neighborsOfFire1, size1, q, fireCells1)


# Bot 2
for q in qList:
   numTrials = numTrialsPerQVal[qList.index(q)]
   for count in range(numTrials):
       print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 2")
       ship2 = Ship()
       size2 = ship2.size
       arr2 = ship2.arr
       bot2 = tuple(ship2.bot)
       button2 = tuple(ship2.button)
       # make lists for tracking burning cells and neighbors of burning cells
       firstCellOnFire2 = tuple(ship2.firstCellOnFire)
       print("This is the button:")
       print(button2)
       print("This is the first cell on fire:")
       print(firstCellOnFire2)
       print("This is start of bot:")
       print(bot2)


       # if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win, so we can
       # stop simulation
       botToButton = findDistanceBetween(bot2[0], bot2[1], button2[0], button2[1], size2, arr2)
       fireToButton = findDistanceBetween(firstCellOnFire2[0], firstCellOnFire2[1], button2[0], button2[1], size2,
                                          arr2)

       if botToButton == -1:
           continue

       if botToButton <= fireToButton:
           print("win: bot is closer")
           winsHashtableBot2[q] = winsHashtableBot2[q] + 1
           continue

       # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
       if q == 1 and botToButton > fireToButton:
           continue

       fireCells2 = [firstCellOnFire2]
       neighborsOfFire2 = getValidOpenVal1(firstCellOnFire2[0], firstCellOnFire2[1], size2, arr2)


       while arr2[bot2[0]][bot2[1]][0] != 2 and arr2[button2[0]][button2[1]][0] != 2:
           # visited[bot2[0], bot2[1]] = 1
           # check if button is only surrounded by closed and on fire cells
           buttonNeighbors = getValidOpen(button2[0], button2[1], size2, arr2, firstCellOnFire2)
           noOpenAroundButton = True
           for neighbor in buttonNeighbors:
               if arr2[neighbor[0]][neighbor[1]][0] == 1:
                   noOpenAroundButton = False
                   break
           if noOpenAroundButton:
               break


           validOpen = getValidOpenVal1(bot2[0], bot2[1], size2, arr2)
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


           print("after moving: Bot 2 " + str(bot2))
           print(bot2)
           if bot2 == button2:
               print("win bc bot reached button")
               winsHashtableBot2[q] = winsHashtableBot2[q] + 1
               break
           spreadFireBot12(arr2, neighborsOfFire2, size2, q, fireCells2)


# Bot 3
for q in qList:
    numTrials = numTrialsPerQVal[qList.index(q)]
    for count in range(numTrials):
        print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 3")
        ship3 = Ship()
        size3 = ship3.size
        arr3 = ship3.arr
        bot3 = tuple(ship3.bot)
        button3 = tuple(ship3.button)

        # make lists for tracking burning cells and neighbors of burning cells
        firstCellOnFire3 = tuple(ship3.firstCellOnFire)
        print("This is the button:")
        print(button3)
        print("This is the first cell on fire:")
        print(firstCellOnFire3)
        print("This is start of bot:")
        print(bot3)
        # if bot spawns closer (or equidistant) to button than the fire does, then bot is guaranteed to win, so we can
        # stop simulation
        botToButton = findDistanceBetween(bot3[0], bot3[1], button3[0], button3[1], size3, arr3)
        fireToButton = findDistanceBetween(firstCellOnFire3[0], firstCellOnFire3[1], button3[0], button3[1], size3,
                                           arr3)

        if botToButton == -1:
            continue

        if botToButton <= fireToButton:
            print("win: bot is closer")
            winsHashtableBot3[q] = winsHashtableBot3[q] + 1
            continue

        # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
        if q == 1 and botToButton > fireToButton:
            continue

        fireCells3 = [firstCellOnFire3]
        # prevFireCells3 = fireCells3
        neighborsOfFire3 = getValidOpenVal1(firstCellOnFire3[0], firstCellOnFire3[1], size3, arr3)
        for neighbor in neighborsOfFire3:
            arr3[neighbor[0]][neighbor[1]][0] = 3  # mark this neighbor as a neighbor of a fire cell

        while arr3[bot3[0]][bot3[1]][0] != 2 and arr3[button3[0]][button3[1]][0] != 2:
            # check if button is surrounded by only closed and on fire cells
            buttonNeighbors = getValidOpen(button3[0], button3[1], size3, arr3, firstCellOnFire3)
            noOpenAroundButton = True
            for neighbor in buttonNeighbors:
                if arr3[neighbor[0]][neighbor[1]][0] == 1:
                    noOpenAroundButton = False
                    break
            if noOpenAroundButton:
                break

            # new stuff starts here:
            distWithout3 = findDistanceBetweenBot3(bot3[0], bot3[1], button3[0], button3[1], size3, arr3)
            listToTraverse = []
            if distWithout3 != -1:
                listToTraverse = getValidOpenVal1(bot3[0], bot3[1], size3, arr3)
            elif findDistanceBetween(bot3[0], bot3[1], button3[0], button3[1], size3, arr3) != -1:
                listToTraverse = getValidOpenVal13(bot3[0], bot3[1], size3, arr3)
            else:
                break

            if listToTraverse:
                distsOpenToButton = []
                preferredList = []
                for neighbor in listToTraverse:
                    neighborToButton = -1
                    preferred = 1
                    if distWithout3 != -1:
                        neighborToButton = findDistanceBetweenBot3(neighbor[0], neighbor[1], button3[0], button3[1],
                                                                   size3, arr3)
                    elif arr3[neighbor[0]][neighbor[1]][0] == 3 and findDistanceBetweenBot3(neighbor[0], neighbor[1], button3[0], button3[1], size3, arr3) != -1:
                        neighborToButton = findDistanceBetweenBot3(neighbor[0], neighbor[1], button3[0], button3[1],
                                                                   size3, arr3)
                        preferred = 2
                    else:
                        neighborToButton = findDistanceBetween(neighbor[0], neighbor[1], button3[0], button3[1], size3,
                                                           arr3)
                        preferred = 3
                    if neighborToButton == -1:  # no path found, so set this val to inf
                        distsOpenToButton.append(float('inf'))
                        preferredList.append(preferred)
                    else:
                        distsOpenToButton.append(neighborToButton)
                        preferredList.append(preferred)

                currPreferred = 3
                smallestIndex = -1
                if distsOpenToButton:
                    smallest = float('inf')
                    count = 0
                    for item in distsOpenToButton:
                        if item < smallest and preferredList[count] <= currPreferred:
                            smallestIndex = count
                            smallest = item
                            currPreferred = preferredList[count]
                        count = count + 1

                if smallestIndex != -1:
                    bot3 = listToTraverse[smallestIndex]
                else:
                    break
            else:
                break
            print("after moving: Bot 3 " + str(bot3))
            print(bot3)
            if bot3 == button3:
                print("win bc bot reached button")
                winsHashtableBot3[q] = winsHashtableBot3[q] + 1
                break
            spreadFireBot3(arr3, neighborsOfFire3, size3, q, fireCells3)


# Bot 4
for q in qList:
   numTrials = numTrialsPerQVal[qList.index(q)]
   for count in range(numTrials):
       print("Q value and count value are as follows: " + str(q) + " " + str(count) + " Bot 4")
       ship4 = Ship()
       size4 = ship4.size
       arr4 = ship4.arr
       bot4 = tuple(ship4.bot)
       button4 = tuple(ship4.button)


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


       if botToButton == -1:
           continue


       if botToButton <= fireToButton:
           print("win: bot is closer")
           winsHashtableBot4[q] = winsHashtableBot4[q] + 1
           continue


       # if q=1 and bot spawns farther from button than the fire, then bot is guaranteed to lose
       if q == 1 and botToButton > fireToButton:
           continue


       fireCells4 = [firstCellOnFire4]
       costDist1F = 2
       costDist2F = 0.75
       # mark the neighbors of the fire cells and the neighbors of the neighbors of the fire cells with weights
       neighborsOfFire4 = getValidOpenVal145(firstCellOnFire4[0], firstCellOnFire4[1], size4, arr4, costDist1F, costDist2F)
       neighborsOfNeighborsFire = []
       for neighbor in neighborsOfFire4:
           arr4[neighbor[0]][neighbor[1]][0] = costDist1F  # mark this neighbor as a neighbor of a fire cell
           listNeighbors = getValidOpenVal145(neighbor[0], neighbor[1], size4, arr4, costDist1F, costDist2F)
           for neighborOfNeighbor in listNeighbors:
               if neighborOfNeighbor not in neighborsOfNeighborsFire and neighborOfNeighbor not in neighborsOfFire4:
                   arr4[neighborOfNeighbor[0]][neighborOfNeighbor[1]][0] = costDist2F
                   neighborsOfNeighborsFire.append(neighborOfNeighbor)


       # mark cells with distance 1, 2, and 3 from the button with respective weights
       dist1FromButton = getValidOpenVal145(button4[0], button4[1], size4, arr4, costDist1F, costDist2F)
       markedCells = [button4]  # keep track of cells already assigned a weight based on distance to button
       benefitButton1 = 0.75
       benefitButton2 = 0.5
       benefitButton3 = 0.25
       for dist1 in dist1FromButton:
           arr4[dist1[0]][dist1[1]][1] = benefitButton1
           markedCells.append(dist1)
           dist2FromButton = getValidOpenVal145(dist1[0], dist1[1], size4, arr4, costDist1F, costDist2F)
           for dist2 in dist2FromButton:
               if dist2 not in markedCells:
                   arr4[dist2[0]][dist2[1]][1] = benefitButton2
                   markedCells.append(dist2)
                   dist3FromButton = getValidOpenVal145(dist2[0], dist2[1], size4, arr4, costDist1F, costDist2F)
                   for dist3 in dist3FromButton:
                       if dist3 not in markedCells:
                           arr4[dist3[0]][dist3[1]][1] = benefitButton3
                           markedCells.append(dist3)


       while arr4[bot4[0]][bot4[1]][0] != 2 and arr4[button4[0]][button4[1]][0] != 2:
           # check if button is surrounded by only closed and on fire cells
           buttonNeighbors = getValidOpen(button4[0], button4[1], size4, arr4, firstCellOnFire4)
           noOpenAroundButton = True
           for neighbor in buttonNeighbors:
               if arr4[neighbor[0]][neighbor[1]][0] != 0:
                   noOpenAroundButton = False
                   break
           if noOpenAroundButton:
               break
           prevCell = bot4
           validOpen = getValidOpenVal145(bot4[0], bot4[1], size4, arr4, costDist1F, costDist2F)


           if validOpen:
               distsOpenToButton = []
               for neighbor in validOpen:
                   neighborToButton = findDistanceBetweenBot4(neighbor[0], neighbor[1], button4[0], button4[1], size4,
                                                              arr4, q, costDist1F, costDist2F, benefitButton1, benefitButton2, benefitButton3)
                   if neighborToButton == -1:  # no path found, so set this val to infinity
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
               if cantReachFromNeighbors(distsOpenToButton):
                   break
           else:
               break
           print("after moving: Bot 4 " + str(bot4))
           print(bot4)
           if bot4 == button4:  # bot2[0] == button2[0] and bot2[1] == button2[1]:
               print("win bc bot reached button")
               winsHashtableBot4[q] = winsHashtableBot4[q] + 1
               break
           spreadFireBot4(arr4, neighborsOfFire4, size4, q, fireCells4, neighborsOfNeighborsFire, costDist1F, costDist2F)
           if bot4 == prevCell: # the bot didn't move, so break
               break




print("bot 1 results:")
for item in winsHashtableBot1:
   index = list(winsHashtableBot1.keys()).index(item)
   print(item, winsHashtableBot1[item] / numTrialsPerQVal[index])


print("bot 2 results:")
for item in winsHashtableBot2:
   index = list(winsHashtableBot2.keys()).index(item)
   print(item, winsHashtableBot2[item] / numTrialsPerQVal[index])


print("bot 3 results:")
for item in winsHashtableBot3:
    index = list(winsHashtableBot3.keys()).index(item)
    print(item, winsHashtableBot3[item] / numTrialsPerQVal[index])

print("bot 4 results:")
for item in winsHashtableBot4:
   index = list(winsHashtableBot4.keys()).index(item)
   print(item, winsHashtableBot4[item] / numTrialsPerQVal[index])


yVals1 = []
for item in winsHashtableBot1:
   index = list(winsHashtableBot1.keys()).index(item)
   yVals1.append(winsHashtableBot1[item] / numTrialsPerQVal[index])


yVals2 = []
for item in winsHashtableBot2:
   index = list(winsHashtableBot2.keys()).index(item)
   yVals2.append(winsHashtableBot2[item] / numTrialsPerQVal[index])

yVals3 = []
for item in winsHashtableBot3:
    index = list(winsHashtableBot3.keys()).index(item)
    yVals3.append(winsHashtableBot3[item] / numTrialsPerQVal[index])

yVals4 = []
for item in winsHashtableBot4:
   index = list(winsHashtableBot4.keys()).index(item)
   yVals4.append(winsHashtableBot4[item] / numTrialsPerQVal[index])


plt.plot(qList, yVals1, label='Bot 1', color='m')
plt.plot(qList, yVals2, label='Bot 2', color='b')
plt.plot(qList, yVals3, label='Bot 3', color='g')
plt.plot(qList, yVals4, label='Bot 4', color='c')

plt.title("Success Rates of Four Bots for Q Values 0-1")
plt.xlabel("Q values (Between 0 and 1)")
plt.ylabel("Success Rate (Between 0 and 1)")
plt.legend(loc='upper right')
plt.show()
