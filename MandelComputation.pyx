#escapecy.pyx
# cython: profile=True  
import cython
import graphicsr
import random

# Def math function from c libraries
cdef extern from "math.h":
    double log(double x)
cdef extern from "math.h":
    double sqrt(double x)

# This struct ensures me to return two variables in escape function
# It's necessary because you can't return two things in one function in c
cdef struct clex:
    double iter_real
    double iter_imag 
    int cur


def hsv_to_rgb(double h, double s, double v):
    # A function that convert hsv coloring to rgb coloring
    if s == 0.0:
        return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
    # Cannot get here



@cython.profile(False) 
cdef inline clex escape(int iteration, double real, double imag):
    # This function is called most often, so it requires a lot of attention to optimize it.
    #  cdef makes this function a c function.
    #  declare the types to allocate the memory for it.
    cdef int j
    cdef int cur = 0
    cdef double iter_real = real
    cdef double iter_imag = imag
    cdef clex newcomplex

    if (iter_real * iter_real + iter_imag * iter_imag) * (8 * (iter_real * iter_real + iter_imag * iter_imag) - 3) <= 0.09375 - iter_real:
        # Check for the second circle
        newcomplex.iter_real = iter_real
        newcomplex.iter_imag = iter_imag
        newcomplex.cur = cur
        return newcomplex
    elif iter_real > -1.25 and iter_real < -0.75 and iter_imag * iter_imag <= (-0.9375 - iter_real * iter_real - 2 * iter_real):
        # Check for the main cardioid
        newcomplex.iter_real = iter_real
        newcomplex.iter_imag = iter_imag
        newcomplex.cur = cur
        return newcomplex
    else:
        for j in xrange(iteration):
            # do the computation.  Note the I have two double variables instead of a complex typed variable
            # That saves a lot of time to compute, because there is no complex type in c.
            if (iter_real * iter_real + iter_imag * iter_imag) <= 9:
                iter_real, iter_imag = (iter_real * iter_real - iter_imag * iter_imag + real,2 * iter_real * iter_imag + imag)
            else:
                cur = j
                break
        newcomplex.iter_real = iter_real
        newcomplex.iter_imag = iter_imag
        newcomplex.cur = cur
        return newcomplex
def modifier(double num, int iteration, double division, double addition):
    # modify a float into a desired range of value
    cdef double hue = num/division + addition


    if hue > 360.0:
        print hue

    while hue< 0.0:
        hue+=1.0

    r,g,b = hsv_to_rgb(hue, 1.0, 1.0)

    return r*255, g*255, b*255
def color_rgb(double r, double g, double b):
    return "#%02x%02x%02x" % (r,g,b)
def colorscheme(num, iteration, double division, double addition):
    cdef double r, g, b
    # return color based on a float
    r,g,b = modifier(num, iteration, division, addition)
    new = color_rgb(r,g,b)
    return new

def colorschemeG(num, iteration, double division, double addition):
    cdef double r, g, b
    # return color based on a float
    # This returns a grey scale value
    r,g,b = modifierG(num, iteration, division, addition)
    new = color_rgb(r,g,b)
    return new
def modifierG(double num, int iteration, double division, double addition):
    # modify a float into a desired range of value
    # For grey scaling
    cdef double hue = num/division + addition


    if hue > 360.0:
        print hue

    while hue< 0.0:
        hue+=1.0

    r,g,b = hsv_to_rgb(hue, 1.0, 1.0)

    return r*255, r*255, r*255
def cvalue(int width, int height, win, int iteration, colors, double division, double addition, background, int color):
    # The function that draws the mandelbrot set.
    cdef int newa
    cdef int newb
    cdef clex newcomplex
    cdef double iter_real, iter_imag, a, ultimate, distance2
    cdef int cur
    cdef double control = width/4.0
    # If the color scheme is color smoothing without mysterious background
    if color == 0 and not background:
        for i in range(height * width):
            newa = i%width - width/2
            newb =  i/width - height/2
            
            real = newa/control
            imag = newb/control


            
            # differentiation of z
            #dz = complex(1, 0)
            newcomplex = escape(iteration, real, imag)
            

            cur = newcomplex.cur

            #b = (dz.real**2 + dz.imag**2)**0.5

            # two different distance method
            #distance = a * math.log(a)/b

            if cur == 0:
                win.plot(newa, newb, 'white')
            else:
                if cur>0:
                    # If not caculated simutanously, it will generate a strange graph. which is where the mysterious background

                    iter_real = newcomplex.iter_real
                    iter_imag = newcomplex.iter_imag
                    iter_real, iter_imag = (iter_real * iter_real - iter_imag * iter_imag + real,2 * iter_real * iter_imag + imag)
                    ultimate = sqrt(iter_real*iter_real + iter_imag*iter_imag)

                    distance2 = cur + 1 - log(log(ultimate))/log(2)
                    # plot the point with color scheme
                    win.plot(newa, newb, colorscheme(distance2, iteration, division, addition))
            if i%(width*30) == 0:
                win.update()
    elif color == 1:
        # If the color scheme is two colors' transformation
        for i in range(height * width):
            newa = i%width - width/2
            newb =  i/width - height/2
            
            real = newa/control
            imag = newb/control

            newcomplex = escape(iteration, real, imag)

            cur = newcomplex.cur

            if cur == 0:
                win.plot(newa, newb, 'white')
            else:
                if cur>0:
                    # If not caculated simutanously, it will generate a strange graph.
                    #iter_real = newcomplex.iter_real
                    #iter_imag = newcomplex.iter_imag
                    # plot the point with selected color scheme
                    win.plot(newa, newb, colors[cur%16])
            if i%(width*30) == 0:
                win.update()
    elif color == 0 and background:
        # If the color scheme selected is smooth coloring and mysterious background
        for i in range(height * width):
            newa = i%width - width/2
            newb =  i/width - height/2

            real = newa/control
            imag = newb/control


            newcomplex = escape(iteration, real, imag)

            cur = newcomplex.cur

            if cur == 0:
                win.plot(newa, newb, 'white')
            else:
                if cur>0:
                    iter_real = newcomplex.iter_real
                    iter_imag = newcomplex.iter_imag
                    iter_real = iter_real * iter_real - iter_imag * iter_imag + real
                    iter_imag = 2 * iter_real * iter_imag + imag
                    ultimate = sqrt(iter_real*iter_real + iter_imag*iter_imag)
                    if ultimate < 1:
                        ultimate = 2
                    distance2 = cur + 1 - log(log(ultimate))/log(2)
                    # plot the point with color scheme
                    win.plot(newa, newb, colorscheme(distance2, iteration, division, addition))

            if i%(width*30) == 0:
                win.update()
    elif color == 2:
        # If the color scheme is grey scale
        for i in range(height * width):
            newa = i%width - width/2
            newb =  i/width - height/2

            real = newa/control
            imag = newb/control

            newcomplex = escape(iteration, real, imag)


            cur = newcomplex.cur

            if cur == 0:
                win.plot(newa, newb, 'white')
            else:
                if cur>0:
                    iter_real = newcomplex.iter_real
                    iter_imag = newcomplex.iter_imag
                    iter_real = iter_real * iter_real - iter_imag * iter_imag + real
                    iter_imag = 2 * iter_real * iter_imag + imag
                    ultimate = sqrt(iter_real*iter_real + iter_imag*iter_imag)
                    if ultimate < 1:
                        ultimate = 2
                    distance2 = cur + 1 - log(log(ultimate))/log(2)
                    # plot the point with color scheme
                    win.plot(newa, newb, colorschemeG(distance2, iteration, division, addition))

            if i%(width*30) == 0:
                win.update()

def zoomin(double ox1, double ox2, double oy1, double oy2, int width, int height, int iteration, frame1, double division, double addition, win, background, colors, int color, p1, p2):
    # Given the current zoom in scale and two corners of the box that is desired to zoom in,
    # This function will caculate the actual square box and then plot the zoom in image and return
    # the current index.
    cdef double iter_x
    cdef double iter_y
    cdef double a
    cdef double nstepx
    cdef double nstepy

    dx = abs(p1.getX() - p2.getX())
    dy = abs(p1.getY() - p2.getY())

    r = min(dx, dy)
    midx = (p1.getX() + p2.getX())/2.0
    midy = (p1.getY() + p2.getY())/2.0
    # Calculate the points of the actual square
    x1 = midx - r/2.0
    x2 = midx + r/2.0
    y1 = midy + r/2.0
    y2 = midy - r/2.0
    stepx = r/width
    stepy = r/height
    # Calculate the steps
    ostepx = (ox2 - ox1)/width
    ostepy = (oy1 - oy2)/height
    newx1 = ox1 + (x1 + width/2.0)*ostepx
    newx2 = ox1 + (x2 + width/2.0)*ostepx
    newy1 = oy2 + (y1 + height/2.0)*ostepy
    newy2 = oy2 + (y2 + height/2.0)*ostepy
    nstepx = (newx2 - newx1)/width
    nstepy = (newy1 - newy2)/height

    print newx1, newx2, newy1, newy2

    iter_y = newy1
    iter_x = 0

    if color == 0 and not background:
        # If the color scheme is color smoothing without mysterious background
        for i in range(height):
            iter_x = newx1
            for t in range(width):
                newa = t - width/2
                newb = height/2 - i

                real = iter_x
                imag = iter_y

                newcomplex = escape(iteration, iter_x, iter_y)

                cur = newcomplex.cur

                if cur == 0:
                    win.plot(newa, newb, 'white')
                else:
                    if cur>0:
                        iter_real = newcomplex.iter_real
                        iter_imag = newcomplex.iter_imag
                        real, imag = (iter_real * iter_real - iter_imag * iter_imag + real,2 * iter_real * iter_imag + imag)
                        ultimate = sqrt(real*real + imag*imag)

                        distance2 = cur + 1 - log(log(ultimate))/log(2)
                        # plot the point with color scheme
                        win.plot(newa, newb, colorscheme(distance2, iteration, division, addition))

                iter_x += nstepx

            if i%(width/28) == 0:
                win.update()

            iter_y -= nstepy
    elif color == 1:
        # If the color scheme is two colors' transformation
        for i in range(height):
            iter_x = newx1
            for t in range(width):
                newa = t - width/2
                newb = height/2 - i

                real = iter_x
                imag = iter_y

                newcomplex = escape(iteration, iter_x, iter_y)

                cur = newcomplex.cur



                if cur == 0:
                    win.plot(newa, newb, 'white')
                else:
                    if cur>0:

                        win.plot(newa, newb, colors[cur%16])

                iter_x += nstepx

            if i%(width/28) == 0:
                win.update()

            iter_y -= nstepy
    elif color == 0 and background:
        # If the color scheme is color smoothing with the mysterious background
        for i in range(height):
            iter_x = newx1
            for t in range(width):
                newa = t - width/2
                newb = height/2 - i

                real = iter_x
                imag = iter_y

                newcomplex = escape(iteration, iter_x, iter_y)

                cur = newcomplex.cur



                if cur == 0:
                    win.plot(newa, newb, 'white')
                else:
                    if cur>0:
                        iter_real = newcomplex.iter_real
                        iter_imag = newcomplex.iter_imag
                        iter_real = iter_real * iter_real - iter_imag * iter_imag + real
                        iter_imag = 2 * iter_real * iter_imag + imag
                        ultimate = sqrt(iter_real*iter_real + iter_imag*iter_imag)
                        if ultimate < 1:
                            ultimate = 2
                        distance2 = cur + 1 - log(log(ultimate))/log(2)
                        # plot the point with color scheme
                        win.plot(newa, newb, colorscheme(distance2, iteration, division, addition))

                iter_x += nstepx

            if i%(width/28) == 0:
                win.update()

            iter_y -= nstepy
    elif color == 2:
        # If the color scheme is grey scale
        for i in range(height):
            iter_x = newx1
            for t in range(width):
                newa = t - width/2
                newb = height/2 - i

                real = iter_x
                imag = iter_y

                newcomplex = escape(iteration, iter_x, iter_y)

                cur = newcomplex.cur



                if cur == 0:
                    win.plot(newa, newb, 'white')
                else:
                    if cur>0:
                        iter_real = newcomplex.iter_real
                        iter_imag = newcomplex.iter_imag
                        iter_real = iter_real * iter_real - iter_imag * iter_imag + real
                        iter_imag = 2 * iter_real * iter_imag + imag
                        ultimate = sqrt(iter_real*iter_real + iter_imag*iter_imag)
                        if ultimate < 1:
                            ultimate = 2
                        distance2 = cur + 1 - log(log(ultimate))/log(2)
                        # plot the point with color scheme
                        win.plot(newa, newb, colorschemeG(distance2, iteration, division, addition))

                iter_x += nstepx

            if i%(width/28) == 0:
                win.update()

            iter_y -= nstepy
    return win, newx1, newx2, newy1, newy2

def inverse(int iteration, int max, c, win):
    # This function use the inverse method to outline the Julia set
    # It's fast but not detailed
    cdef double a
    cdef double b
    cdef double ran
    cdef double d1,d2
    # Pick a random point in the graph
    a = random.random() * max * 2.0 - max
    b = random.random() * max * 2.0 - max

    z = complex(a,b)
    for i in xrange(iteration):
        # Choose whether to use the negative value or positive
        ran = random.random()
        d1 = abs((z - c)**0.5 - c)**2
        d2 = abs(-1 * (z - c)**0.5 - c)**2

        if ran>0.5:
            z = (z - c)**0.5
            win.plot(z.real*100, z.imag*100, 'green')
        elif ran < 0.5:
            z = -1 * (z - c)**0.5
            win.plot(z.real*100, z.imag*100, 'red')

def bruteForce(int iteration, win, int width, int height, double creal, double cimag, double division,double addition):
    # This function use the brute force method to compute the Julia set
    # It iteratively goes through each point in the window and caculates whether the point escapes or not.
    cdef int newa, newb
    cdef double dreal, dimag, real, imag, iter_real, iter_imag
    cdef int cur
    for i in range(height * width):
        dreal = 1.0
        dimag = .0
        newa = i%width - 200
        newb = i/width - 200
        iter_real = newa/100.0
        iter_imag = newb/100.0


        cur = 0
        for j in range(iteration):
            if (iter_real**2 + iter_imag**2) <= 4:
                iter_real, iter_imag = (iter_real*iter_real - iter_imag * iter_imag + creal, 2 * iter_real * iter_imag + cimag)

            else:
                cur = j
                break
        a = (iter_real*iter_real + iter_imag*iter_imag)

        if a <= 4:
            win.plot(newa, newb, 'white')
        else:
            if cur>0:
                real, imag = (iter_real * iter_real - iter_imag * iter_imag + creal,2 * iter_real * iter_imag + cimag)
                ultimate = sqrt(real*real + imag*imag)

                distance2 = cur + 1 - log(log(ultimate))/log(2)
                # plot the point with color scheme
                win.plot(newa, newb, colorschemeG(distance2, iteration, division, addition))
