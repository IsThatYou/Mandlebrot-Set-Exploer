__author__ = 'Wangj1'
# Written by Junlin Wang
import graphics
import random
import math
import colorsys
def julia(z, c):
    return z**2+c
def inverseJulia(z, c):
    return (z - c)**0.5
def colorlist(num):
        # make a random color list for a given index
        colorl = []
        for i in range(num):
            color = graphics.color_rgb(random.randrange(80,256), random.randrange(1,256), random.randrange(80, 256))
            colorl.append(color)
        return colorl
def colorlist2(color1, color2, num):
    r1 = int(color1[1:3], 16)
    g1 = int(color1[3:5], 16)
    b1 = int(color1[5:7], 16)
    r2 = int(color2[1:3], 16)
    g2 = int(color2[3:5], 16)
    b2 = int(color2[5:7], 16)
    rlist = []
    glist = []
    blist = []
    colors = []
    for i in range(min(r1, r2), max(r1, r2), (max(r1, r2) - min(r1, r2))/num):
        rlist.append(i)
    for i in range(min(g1, g2), max(g1, g2), (max(g1, g2) - min(g1, g2))/num):
        glist.append(i)
    for i in range(min(b1, b2), max(b1, b2), (max(b1, b2) - min(b1, b2))/num):
        blist.append(i)
    for i in range(num):
        color = graphics.color_rgb(rlist[i], glist[i], blist[i])
        colors.append(color)
    return colors
def colorlist3(color, num, smooth):
    # single color
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    colors = []

    if smooth:
        rstep = (256 - r)/num
        gstep = (256 - g)/num
        bstep = (256 - b)/num
    else:
        rstep = r/num
        gstep = g/num
        bstep = b/num

    if not smooth:
        for i in range(num):
            new = graphics.color_rgb(r - rstep * i, g - gstep * i, b - bstep * i)
            colors.append(new)
    else:
        for i in range(num):
            new = graphics.color_rgb(r + rstep * i, g + gstep * i, b + bstep * i)
            colors.append(new)

    return colors
def modifier(num, iteration):
    # modify a float into a desired range of value

    hue = num/40.0 + 0.51


    if hue > 360.0:
        print (hue)

    while hue< 0.0:
        hue+=1.0
    r,g,b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    return r*255, g*255, b*255

def colorscheme(num, iteration):
    # return color based on a float
    r,g,b = modifier(num, iteration)
    new = graphics.color_rgb(r,g,b)
    return new

def grayscale(max, cur):
    step = 256/max
    magnitude = int(cur * step)

    color = graphics.color_rgb(0.21 * magnitude, 0.72 * magnitude, 0.07 * magnitude)
    return color

def inverse(iteration, max, c, win):

    a = random.random() * max * 2.0 - max
    b = random.random() * max * 2.0 - max
    z = complex(a,b)
    for i in xrange(iteration):
        ran = random.random()
        d1 = abs(inverseJulia(z, c) - c)**2
        d2 = abs(-1 * inverseJulia(z, c) - c)**2

        if ran >= d2/(d1 + d2):
            z = inverseJulia(z, c)
            win.plot(z.real*100, z.imag*100, 'green')
        elif ran< d2/(d1 + d2):
            z = -1 * inverseJulia(z, c)
            win.plot(z.real*100, z.imag*100, 'red')

def bruteForce(iteration, win, width, height, c, colors):

    for i in range(height * width):
        dz = complex(1, 0)
        newa = i%width - 400
        newb = i/width - 400
        z = complex(newa/100.0, newb/100.0)
        iter_z = z
        color = 'white'
        cur = 0
        for j in range(iteration):
            if (iter_z.real**2 + iter_z.imag**2)**0.5 <= 2:
                iter_z = julia(iter_z,c)
                dz = 2 * iter_z * dz
            else:
                cur = j
                break
        b = (dz.real**2 + dz.imag**2)**0.5
        a = (iter_z.real**2 + iter_z.imag**2)**0.5
        distance = a * math.log(a)/b
        color2 = grayscale(10, distance)

        if a <= 2:
            win.plot(z.real*100, z.imag*100, color)
        else:
            if cur>0:

                win.plot(z.real*100, z.imag*100, colors[(cur-1)%16])#colors[(cur-1)%16]
        if i%width == 0:
            win.update()



# randomly choose z0
# iterate T^-1 a lot without plotting flip a coin to choose negative square root or positive
# iterate a lot and plot results
def main():
    iteration = 1000
    width = 800
    length = 800
    win = graphics.GraphWin('Julia Set', width, length, autoflush=False)
    win.setBackground('black')
    win.setCoords(-400, -400, 400, 400)
    max = 4.0
    c = complex( 0.285, 0.01)
    inverse(iteration, max, c, win)
    colors = colorlist3('#2EA9DF',16, True)
    #bruteForce(iteration/10, win, width, length, c, colors)
    win.getMouse()


if __name__ == "__main__":
    main()