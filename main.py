import numpy as np

#rows, cols, elements = (5, 5, 2)
#arr = [[[0 for _ in range(elements)] for _ in range(cols)] for _ in range(rows)]
size = 5

arr = np.zeros((size, size, 2))

arr[4][3][1] = 1

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
randRow = np.random.randint(0, size)
randCol = np.random.randint(0, size)

arr[randRow][randCol] = [1, 0]


