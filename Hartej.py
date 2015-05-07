__author__ = 'Wangj1'
# Written by Junlin Wang
from graphics import *
from cmath import *
g = GraphWin('name', 600,600, False)
def main():
    g.setBackground('black')
    g.setCoords(-2,-2,2,2)
    iterate()
    g.getMouse()
def iterate():
    a= -2
    while a<=2:
        b = -2
        while b<=2:
            z = complex (a, b)
            c = complex (a, b)
            counter = 0
            if counter<100:
                z = z*z + c
                g.plot(z.real, z.imag, 'white')
            counter += 1
            b += .01
        a+=.01
if __name__ == "__main__":
    main()