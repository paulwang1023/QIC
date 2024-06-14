import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import math


n = 5 # size of space: n x n must be odd
c = 8   # 
p = 0.005 # probability of initially panicky individuals
s = 1
color = "0, G, Y, R, RG, BY, B, M"


cd_base = {"R":[0.8, 0, 0], "G":[0, 0.4, 0], "B":[0, 0, 0.8], "0":[0, 0, 0], "1":[1, 1, 1],
        "C":[0, 0.8, 0.8],
        "Y":[0.4, 0.4, 0],
        "M":[0.8, 0, 0.8], "RG":[0.4, 0.8, 0], "RY":[1, 0.8, 0],
        "BG":[0, 0.8, 0.4], "BY":[0.8, 0.8, 0.4], }

cd = [cd_base[i] for i in color.split(", ")]

def initialize():
    global config, timestep, Xerror, Zerror, detect, correct, last_error, errors
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            if (x+y)%2 == 0:
                config[x, y] = 0
            elif x%2 == 0:
                config[x, y] = 1
            else:
                config[x, y] = 2
                
    timestep = 0
    Xerror = zeros([n, n])
    Zerror = zeros([n, n])
    detect = zeros([n, n])
    correct = [0]*((n*n+1)//2)
    last_error = -1
    errors = []

def observe():
    global config, timestep, Xerror, Zerror, detect, correct
    cla()
    img = zeros([n, n, 3])
    for x in range(n):
        for y in range(n):
            for k in range(3):
                if (x+y)%2 == 0:
                    if Xerror[x, y]:
                        if Zerror[x, y]:
                            img[x, y, k] = cd[7][k]
                        else:
                            img[x, y, k] = cd[3][k]
                    elif Zerror[x, y]:
                        img[x, y, k] = cd[6][k]
                    else:
                        img[x, y, k] = cd[int(config[x, y])][k]
                elif x%2 == 0:
                    img[x, y, k] = cd[4][k] if detect[x, y] else cd[int(config[x, y])][k]
                else:
                    img[x, y, k] = cd[5][k] if detect[x, y] else cd[int(config[x, y])][k]
    imshow(img, vmin = 0, vmax = 1)

def update_random():
    global config, timestep, Xerror, Zerror, detect, correct
    for x in range(n):
        for y in range(n):
            detect[x, y] = 0
            for i in [Xerror, Zerror]:
                if random() < p and (x + y) % 2 == 0:
                    i[x, y] = not i[x, y]
                    # print(x, y)
            

def neighbor(x, y):
    if x == 0:
        if y == 0:
            return [[1, 0], [0, 1]]
        if y == n-1:
            return [[1, 0], [0, -1]]
        return [[1, 0], [0, 1], [0, -1]]
    if x == n-1:
        if y == 0:
            return [[-1, 0], [0, 1]]
        if y == n-1:
            return [[-1, 0], [0, -1]]
        return [[-1, 0], [0, 1], [0, -1]]
    if y == 0:
        return [[-1, 0], [1, 0], [0, 1]]
    if y == n-1:
        return [[-1, 0], [1, 0], [0, -1]]
    return [[-1, 0], [1, 0], [0, 1], [0, -1]]

def update_detect():
    global config, timestep, Xerror, Zerror, detect, correct
    for x in range(n):
        for y in range(n):
            for i in [Xerror, Zerror]:
                if (x+y)%2 != 0:
                    if (x%2 == 0 and i is Xerror) or (x%2 != 0 and i is Zerror):
                        detect[x, y] = 0
                        for p in neighbor(x, y):
                            if i[x+p[0], y+p[1]]:
                                detect[x, y] = not detect[x, y]


table7 = [  [0,0], [0,2], [0,4], [0,6],
            [1,1], [1,3], [1,5], 
            [2,0], [2,2], [2,4], [2,6],
            [3,1], [3,3], [3,5], 
            [4,0], [4,2], [4,4], [4,6],
            [5,1], [5,3], [5,5], 
            [6,0], [6,2], [6,4], [6,6]
            ]
table5 = [  [0,0], [0,2], [0,4],
            [1,1], [1,3], 
            [2,0], [2,2], [2,4],
            [3,1], [3,3], 
            [4,0], [4,2], [4,4]
            ]
table3 = [  [0,0], [0,2],
            [1,1], 
            [2,0], [2,2]
            ]

def test(type):
    global detect, correct
    test = zeros([n, n])
    terr = zeros([n, n])
    '''
    for i in range(len(correct)):
        x, y = 0, 0
        if i % n > n/2:
            y = int(2*i//n+1)
            x = int(1+2*(i % n - (n+1)/2))
        else:
            y = int(2*i//n)
            x = int(2*(i % n))
        terr[x, y] = correct[i]
    '''
    for i in range(len(correct)):
        terr[table5[i][0], table5[i][1]] = correct[i]
    for x in range(n):
        for y in range(n):
            if (x+y)%2 != 0:
                if (x%2 == 0 and type == "X") or (x%2 != 0 and type == "Z"):
                    test[x, y] = 0
                    for p in neighbor(x, y):
                        if terr[x+p[0], y+p[1]]:
                            test[x, y] = not test[x, y]
                    if test[x, y] != detect[x, y]:
                        return False
    return True
                    
    for i in range(len(correct)):
        x, y = 0, 0
        if i % n > n/2+1:
            y = int(2*i//n+1)
            x = int(1+2*(i % n - (n+1)/2))
        else:
            y = int(2*i//n)
            x = int(2*(i % n))
        for p in neighbor(x, y):
            if i[x+p[0], y+p[1]]:
                detect[x, y] = not detect[x, y]


def combination(i, j):
    if j == 0:
        return [[0]*i]
    if i == j:
        return [[1]*i]
    return [x+[1] for x in combination(i-1,j-1)] + [x+[0] for x in combination(i-1, j)]


def recursion(i, type):
    global detect, correct
    for m in range(len(correct)):
        for correct in combination(len(correct), m):
            # print(correct)
            if test(type):
                return True
    return False


    """
    if i == len(correct):
        return test(type)
    correct[i] = 0
    if not recursion(i+1, type):
        correct[i] = 1
        return recursion(i+1, type)
    return True
    """

def update_correct():
    global config, timestep, Xerror, Zerror, detect, correct
    recursion(0, "X")
    # print("CORRECT:\n",correct)
    for i in range(len(correct)):
        if correct[i]:
            Xerror[table5[i][0], table5[i][1]] = not Xerror[table5[i][0], table5[i][1]]
    recursion(0, "Z")
    for i in range(len(correct)):
        if correct[i]:
            Zerror[table5[i][0], table5[i][1]] = not Zerror[table5[i][0], table5[i][1]]
    '''
    for i in range(len(correct)):
        x, y = 0, 0
        if i % n > n/2:
            y = int(2*i//n+1)
            x = int(1+2*(i % n - (n+1)/2))
        else:
            y = int(2*i//n)
            x = int(2*(i % n))
        if correct[i]:
            Xerror[x, y] = not Xerror[x, y]
    '''
    '''
    recursion(0, "Z")
    for i in range(len(correct)):
        x, y = 0, 0
        if i % n > n/2:
            y = int(2*i//n+1)
            x = int(1+2*(i % n - (n+1)/2))
        else:
            y = int(2*i//n)
            x = int(2*(i % n))
        if correct[i]:
            Zerror[x, y] = not Zerror[x, y]
    '''
    for x in range(n):
        for y in range(n):
            detect[x, y] = 0
            


def update():
    global config, nextconfig, timestep, Xerror, Zerror, detect, correct, last_error, errors, count
    if timestep % 3 == 0:
        Xerror = zeros([n, n])
        Zerror = zeros([n, n])
        update_random()
    if timestep % 3 == 1:
        update_detect()
    if timestep % 3 == 2:
        update_correct()
        TestX = []
        for x in range(n):
            for y in range(n):
                if Xerror[x, y]:
                    TestX.append([x, y])
        TestZ = []
        for x in range(n):
            for y in range(n):
                if Zerror[x, y]:
                    TestZ.append([x, y])
        if len(TestX)+len(TestZ):
            errors.append((timestep-last_error)/3)
            count += 1
            print("ERROR: ", count, (timestep-last_error)/3, TestX+TestZ)
            last_error = timestep
                    


    timestep = timestep + 1


count = 0
import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])


'''
for p in [0.008+0.0001*x for x in range(20)]:
    count = 0
    initialize()
    while(count < 2000):
        update()
    print(round(float(sum(errors)/len(errors)),4),",")
    #print("P=", round(float(p),6), "RESULT:",round(float(sum(errors)/len(errors)),4), "Compare:", round(1/p,4))
'''