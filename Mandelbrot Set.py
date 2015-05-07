__author__ = 'Wangj1'
# Written by Junlin Wang

import graphics
import JuliaSet
import math
import colorsys
import pstats
import cProfile

import pyximport; pyximport.install()
import escapecy



def mandle(z, c):
    return z**2 + c
def escape(iteration, iter_z, c):
    cur = 0
    for j in xrange(iteration):
        if (iter_z.real**2 + iter_z.imag**2)**0.5 <= 3:
            iter_z = mandle(iter_z,c)
            #dz = 2 * iter_z * dz
        else:
            cur = j
            break
    return iter_z, cur
def cvalue(width, height, win, iteration, control, colors):
    for i in range(height * width):
        newa = i%width - 400
        newb =  i/width - 400
        c = complex(newa/control, newb/control)
        z = 0 + c
        iter_z = z
        color = 'white'
        cur = 0
        # differentiation of z
        #dz = complex(1, 0)
        iter_z, cur = escape(iteration, iter_z, c)
        #b = (dz.real**2 + dz.imag**2)**0.5
        a = (iter_z.real**2 + iter_z.imag**2)**0.5
        # two different distance method
        #distance = a * math.log(a)/b

        if a <= 2:
            win.plot(z.real*control, z.imag*control, color)
        else:
            if cur>0:
                distance2 = cur + 1 - math.log(math.log(abs(mandle(iter_z,c))), 2)
                win.plot(z.real*control, z.imag*control, colorscheme(distance2, iteration))
        if i%(width*30) == 0:
            win.update()

def modifier(num, iteration):
    # modify a float into a desired range of value

    hue = num/40.0 + 0.53


    if hue > 360.0:
        print hue

    while hue< 0.0:
        hue+=1.0
    r,g,b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return r*255, g*255, b*255

def colorscheme(num, iteration):
    # return color based on a float
    r,g,b = modifier(num, iteration)
    new = graphics.color_rgb(r,g,b)
    return new

def zoomin(ox1, ox2, oy1, oy2, height, width, iteration, win):

    p1 = win.getMouse()
    print p1.getX(), p1.getY()
    print("first point")
    p2 = win.getMouse()
    print p2.getX(), p2.getY()
    print("second point")

    dx = abs(p1.getX() - p2.getX())
    dy = abs(p1.getY() - p2.getY())
    r = min(dx, dy)
    midx = (p1.getX() + p2.getX())/2.0
    midy = (p1.getY() + p2.getY())/2.0
    x1 = midx - r/2.0
    x2 = midx + r/2.0
    y1 = midy + r/2.0
    y2 = midy - r/2.0
    stepx = r/width
    stepy = r/height

    ostepx = (ox2 - ox1)/width
    ostepy = (oy1 - oy2)/height
    newx1 = ox1 + (x1 + 400.0)*ostepx
    newx2 = ox1 + (x2 + 400.0)*ostepx
    newy1 = oy2 + (y1 + 400.0)*ostepy
    newy2 = oy2 + (y2 + 400.0)*ostepy
    nstepx = (newx2 - newx1)/width
    nstepy = (newy1 - newy2)/height
    print nstepx, nstepy
    print newx1, newx2, newy1, newy2

    iter_y = newy1
    iter_x = 0
    box = graphics.Rectangle(graphics.Point(x1, y1), graphics.Point(x2, y2))
    box.draw(win)
    win = graphics.GraphWin('Mandlebrot Exploerer', width, height, autoflush=False)
    win.setBackground('black')
    win.setCoords(-400, -400, 400, 400)
    for i in range(height):
        iter_x = newx1
        for t in range(width ):
            newa = t - 400
            newb = 400 - i

            c = complex(iter_x, iter_y)
            z = 0 + c
            iter_z = z
            cur = 0

            for j in range(iteration):
                if (iter_z.real**2 + iter_z.imag**2)**0.5 <= 3:
                    iter_z = mandle(iter_z,c)
                    #dz = 2 * iter_z * dz
                else:
                    cur = j
                    break
            #b = (dz.real**2 + dz.imag**2)**0.5
            a = (iter_z.real**2 + iter_z.imag**2)**0.5
            # two different distance method
            #distance = a * math.log(a)/b

            if a <= 2:
                win.plot(newa, newb, 'white')
            else:
                if cur>0:
                    distance2 = cur + 1 - math.log(math.log(abs(mandle(iter_z,c))), 2)
                    win.plot(newa, newb, colorscheme(distance2, 100))
            if i%width == 0:
                win.update()
            '''
            if iter_x < newx2:
                iter_x += ostepx
            elif iter_x >= newx2:

                iter_x = newx1
                iter_y -= ostepy
            '''
            iter_x += nstepx
        iter_y -= nstepy
    print iter_x, iter_y
    return win, newx1, newx2, newy1, newy2






def main():
    width = 800
    height = 800
    win = graphics.GraphWin('Mandlebrot Exploerer', width, height, autoflush=False)
    win.setCoords(-400, -400, 400, 400)
    win.setBackground('black')
    colors = JuliaSet.colorlist(16)
    cvalue(width, height,win, 100, 200.0, colors)
    ox1 = -2.0
    ox2 = 2.0
    oy1 = 2.0
    oy2 = -2.0
    '''
    while True:
        print("zoom in begin")
        win, ox1, ox2, oy1, oy2 = zoomin(ox1, ox2, oy1, oy2, width, height, 100, win)
    '''
if __name__ == "__main__":
    cProfile.run("main()", "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats(10)
