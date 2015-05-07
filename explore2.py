__author__ = 'Wangj1'
# Written by Junlin Wang
#for every value of R:
# 1. genrate a radom X0 between 0, 1
# 2. Iterate a large transient number of iterations without plotting anything
# 3. Iterate some numbers of subsequent iterations and plot Xn as a function of R
# Chaos: deterministic, bounded, aperiodic, sensitive dependent on initial condition.
# filled julia set of T, is the set of all initial numbers that is bounded. (not blow up)
# julia set is the boundary of filled julia set.
from graphics import *
import random
def logisticmap(x, r, iteration):
    orbit = []
    for i in range(iteration):
        sum = r * x *(1-x)
        x = sum
        orbit.append(sum)

    return orbit
# doesn't work
def logisticmap2(x, r, iteration):
    orbit = logisticmap(x, r, iteration)
    pet = orbit[-1]
    counter = 0
    start = 0
    end = 0
    for i in range(iteration):
        print orbit[i], orbit[-1]
        if '%0.7f'%(orbit[i]) == '%0.7f'%(orbit[-1]):
            start = i
            counter += 1
        if counter == 2:
            end = i

    if start == end:
        return [orbit[-1]]
    else:
        return orbit[int(start):int(end)]
# doesn't work
def interpret(x, y):
    x *= 1000
    y *= 1000
    tenx = 1
    teny = 1
    x0 = x
    y0 = y
    while int(x0) < x0:
        x0 *= 10
        tenx *= 10

    while int(y0) < y0:
        y0 *= 10
        teny *= 10
    if tenx > teny:
        y *= tenx
        x *= tenx
    elif teny > tenx:
        y *= teny
        x *= teny
    elif tenx == teny:
        y *= tenx
        x *= teny
    return int(x/2), int(y/2)
def zoomin(p,x, y, win, level):
    coordx1 = (p.getX() - x/4) * 2
    coordx2 = (p.getX() + x/4) * 2
    coordy1 = (p.getY() - y/4) * 2
    coordy2 = (p.getY() + y/4) * 2
    win = GraphWin('Chaotic Explorer', 1000, 500)
    win.setBackground('black')
    win.setCoords(coordx1, coordy1, coordx2, coordy2)
    x1 = coordx1/(250.0 * 2**(level))
    x2 = coordx2/(250.0 * 2**(level))
    rate = (x2 - x1)/1000
    print p.getX(), p.getY()
    print x1, x2
    r = x1
    iteration = 100
    drawlist = []
    for i in range(1000):
        r += rate
        if r > 4.0:
            drawlist.append(0)
        else:
            a = logisticmap(random.random(), r, iteration)
            a = a[80::]
            drawlist.append(a)
    for i in range(int(coordx1), int(coordx2)):

        b = drawlist[i - int(coordx1)]
        if b == 0:
            pass
        else:
            for z in b:

                win.plot(i, z * 500 * 2**level,'white')
    return win


def main():
    #4.751, 4.6562, 4.6683, 4.6686, 4.6692
    win = GraphWin("Chaotic Explorer", 1000, 500)
    win.setBackground('black')
    iteration = 100
    x1 = 0.0
    x2 = 4.0
    coord1 = 0
    coord2 = 1000
    win.setCoords(coord1, 0, coord2, 500) # 2400, 4000 is too big
    rate = (x2 - x1)/1000
    r = x1
    drawlist = []
    for j in range(1000):
        r +=rate
        a = logisticmap(random.random(), r,iteration) # 1000/2
        a = a[80::]
        drawlist.append(a) #can be optimized

    for i in range(int(coord1), int(coord2)):

        b = drawlist[i - coord1]
        for z in b:

            win.plot(i, z * 500,'white')
    zoominlevel = 1

    while True:
        p = win.getMouse()
        win = zoomin(p, 1000, 500, win, zoominlevel)
        zoominlevel += 1
main()




