__author__ = 'Wangj1'
# Zn+1 = Zn - (Z^4 - 1)/4Z^3
import graphics

def newton(z):
    try:
        new_z = z - (z**4 - 1)/(4 * z**3)
    except ZeroDivisionError:
        return z
    return new_z
def dbtp(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5
def distance(z):
    real = z.real
    imag = z.imag

    d1 = dbtp(real, imag, 1, 0)
    d2 = dbtp(real, imag, 0, -1)
    d3 = dbtp(real, imag, -1, 0)
    d4 = dbtp(real, imag, 0, 1)

    dmin = min(d1, d2, d3, d4)

    if dmin == d1:
        return "red"
    if dmin == d2:
        return "blue"
    if dmin == d3:
        return "yellow"
    if dmin == d4:
        return "green"
    return "white"



width = 800
height = 800
iteration = 50
win = graphics.GraphWin("Newton's Law Exploer", width, height, autoflush=False)

win.setCoords(-400, -400, 400, 400)


for i in range(width):
    for j in range(height):
        a = (i - 400.0)/200.0
        b = (j - 400.0)/200.0
        z = complex(a, b)
        for c in range(iteration):
            z = newton(z)
        color = distance(z)
        win.plot(i - 400, j - 400, color)

win.getMouse()
win.close()