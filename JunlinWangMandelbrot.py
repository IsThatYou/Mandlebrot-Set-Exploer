#!/usr/bin/python3
__author__ = 'Wangj1'
# Written by Junlin Wang

import graphics
import JuliaSet
import math
import colorsys
import pstats
import cProfile
import graphicsr
try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
import time
import pyximport; pyximport.install()
import MandelComputation

class Great:
    def __init__(self, master, menubar):
        self.master = master
        # For the zoom in method
        self.clicks = []
        self.clicksCount = 0

        # The menu bar
        filemenu = tk.Menu(menubar)
        # This saves the mandelbrot set into a eps file at the same directory, and then the users can convert it
        # into whatever format they want
        filemenu.add_command(label="Save Mandelbrot", command=self.save)
        # This contains the instruction necessary to play with the program
        filemenu.add_command(label="Help", command = self.help)
        menubar.add_cascade(label="File", menu=filemenu)



        # Frames
        self.frame1 = tk.Frame(self.master)
        self.frame2 = tk.Frame(self.master)
        self.frame3 = tk.Frame(self.frame1)
        self.frame4 = tk.Frame(self.frame1)
       
        self.frame1.grid(row = 0, column = 0)
        self.frame2.grid(row = 0, column = 1)

        '''''''Mandlebrot Set'''''''
        # Default color scheme
        self.colorScheme1 = True
        # Another color scheme
        self.colorScheme2 = False
        # Yet another color scheme
        self.colorScheme3 = False


        self.abackground = False
        self.width = 400
        self.height = 400
        # The arguments for zoom in method
        self.ox1 = -1.0 * self.width/200
        self.ox2 = 1.0 * self.width/200
        self.oy1 = 1.0 * self.height/200
        self.oy2 = -1.0 * self.height/200

        
        self.iteration = 1000
        # The graphwin window
        self.win = graphicsr.GraphWin(self.frame1, self.width, self.height, autoflush=False)
        # Press and drag to get the Julia set with current C value
        self.win.bind("<B1-Motion>", lambda x: self.drawJulia(x))
        # Double click two corners to zoom in
        self.win.bind("<Double-Button-1>", lambda x: self.accumulation(x))
        self.win.setCoords(-1 * self.width/2, -1 * self.height/2, self.width/2, self.height/2)
        self.win.setBackground('black')
        self.colors = JuliaSet.colorlist(16)

        # I have three color options: color smoothing, two colors' transformation, and grey scale
        self.title = tk.Label(self.frame1, text = "Mandlebrot Exploer", foreground = '#D0104c', font = 'gothics')
        self.iterationLabel = tk.Label(self.frame1, text = "Iteration:", font = "Times")
        self.iterationEntry = tk.Entry(self.frame1)
        self.iterationEntry.insert(0, "1000")
        self.iterationEntry.config(width = 8)
        # The buttons that switch color mode
        self.colorOption1 = ttk.Button(self.frame1, text = "Color OptionI", command = self.colorChange1)
        self.colorOption2 = ttk.Button(self.frame1, text = "Color OptionII", command = self.colorChange2)
        self.colorOption3 = ttk.Button(self.frame1, text = "Color OptionIII", command = self.colorChange3)
        self.colorOptionl1 = tk.Label(self.frame3, text = "Smooth Coloring", foreground = "#2EA9DF", font = ("Helvetica", 12))
        self.colorOptionl2 = tk.Label(self.frame3, text = "Two Color Converging", font = ("Helvetica", 12),foreground = "#2EA9DF")
        self.colorOptionl3 = tk.Label(self.frame3, text = "Grey Scale", font = ("Helvetica", 12), foreground = "#2EA9DF")

        self.division = ttk.Scale(self.frame3, from_= 0.0, to = 100.0, orient = 'horizontal')
        self.addition = ttk.Scale(self.frame3, from_= 0.0, to = 1.0, orient = 'horizontal')
        self.colorLabel = tk.Label(self.frame3, text = "Color Options")
        # set the initial scale values
        self.division.set(40.0)
        self.addition.set(0.51)
        self.addLabel = tk.Label(self.frame3, text = "Smooth Change", font = "TImes")
        self.divLabel = tk.Label(self.frame3, text = "Color Change", font = "Times")
        # The create button
        self.submitButton1 = ttk.Button(self.frame4, text = "Create", command = self.submit1)
        # The apply button
        self.submitButton2 = ttk.Button(self.frame4, text = "Apply", command = self.apply)
        self.refineJButton = ttk.Button(self.frame4, text = "Refine Julia Set", command = self.refine)
        self.bvar = tk.IntVar(self.master)
        self.BackCheck = ttk.Checkbutton(self.frame3, text = "Mysterious Background", variable =  self.bvar)

        self.divisionG = ttk.Scale(self.frame3, from_= 0.0, to = 100.0, orient = 'horizontal')
        self.additionG = ttk.Scale(self.frame3, from_= 0.0, to = 1.0, orient = 'horizontal')

        self.divisionG.set(40.0)
        self.additionG.set(0.51)
        self.divisionGLabel = ttk.Label(self.frame3, text = "Smooth", font = "Times")
        self.additionGLabel = ttk.Label(self.frame3, text = "Value", font = "Times")
        self.colLabel1 = tk.Label(self.frame3, text = "Color 1 (Hex)", font = "Times")
        self.colLabel2 = tk.Label(self.frame3, text = "Color 2 (Hex)", font = "Times")
        self.col1 = tk.Entry(self.frame3)
        self.col2 = tk.Entry(self.frame3)
        self.col1.config(width = 25)
        self.col2.config(width = 25)
        self.col1.insert(0, "#2EA9DF")
        self.col2.insert(0, "#DDD23B")

        # Window Griding
        self.win.grid(row = 0, column = 0, rowspan = 35)
        self.title.grid(row = 0, column = 1, columnspan = 3)
        self.iterationLabel.grid(row = 1, column = 1)
        self.iterationEntry.grid(row = 1, column = 2)

        # Color Option Griding
        self.colorOption1.grid(row = 2, column = 1)
        self.colorOption2.grid(row = 2, column = 2)
        self.colorOption3.grid(row = 2, column = 3)

        self.colorOptionl1.grid(row = 1, column = 1, columnspan = 3)
        self.frame3.grid(row= 3, column = 1, columnspan = 4)
        self.addLabel.grid(row = 2, column = 1, columnspan = 3)
        self.division.grid(row = 3, column = 0, columnspan = 5)
        self.divLabel.grid(row = 4, column = 1, columnspan = 3)
        self.addition.grid(row = 5, column = 0, columnspan = 5)
        self.BackCheck.grid(row = 6, column = 0, columnspan = 4)

        self.frame4.grid(row = 4, column = 1, columnspan = 4)
        self.submitButton1.grid(row = 0, column = 1, columnspan = 1)
        self.submitButton2.grid(row = 0, column = 0)
        self.refineJButton.grid(row = 1, column = 0, columnspan = 2)



        '''Julia Set'''
        self.width2 = 400
        self.height2 = 400
        self.win2 = graphicsr.GraphWin(self.frame2, self.width2, self.height2, autoflush=False)
        self.win2.setCoords(-1 * self.width/2, -1 * self.height/2, self.width/2, self.height/2)
        self.win2.setBackground('black')

        self.win2.grid(row = 0, column = 0, rowspan = 35)

    def apply(self):
        # This method applies the current color scheme selected to the current graph.
        # It differs from create because instead of giving a brand new Mandelbrot Set,
        # It gives the current graph.
        self.win = graphicsr.GraphWin(self.frame1, self.width, self.height, autoflush=False)
        self.win.setBackground('black')
        # Press and drag to get the Julia set with current C value
        self.win.bind("<B1-Motion>", lambda x: self.drawJulia(x))
        # Double click two corners to zoom in
        self.win.bind("<Double-Button-1>", lambda x: self.accumulation(x))
        self.win.setCoords(-1 * self.width/2, -1 * self.height/2, self.width/2, self.height/2)
        self.win.grid(row = 0, column = 0, rowspan = 35)
        color = 0
        # Determine what color scheme to use
        if self.colorScheme1 == True:
            color = 0
        elif self.colorScheme2 == True:
            color = 1
        elif self.colorScheme3 == True:
            color = 2
        # Determine whether to use the mysterious background
        self.abackground = self.bvar.get()
        colors = self.colorscheme2(self.col1.get(), self.col2.get(), 16)
        width = self.width
        height = self.height
        p1 = graphicsr.Point(self.ox1*100, self.oy1*100)
        p2 = graphicsr.Point(self.ox2*100, self.oy2*100)
        # I use zoom in with the current graph's corners so it doesn't change the zoom but can update the color
        self.win, self.ox1, self.ox2, self.oy1, self.oy2 = MandelComputation.zoomin(self.ox1, self.ox2, self.oy1, self.oy2, width, height, 100, self.frame1, self.division.get(), self.addition.get(), self.win, self.abackground,  colors, color, p1, p2)


    def submit1(self):
        # This draws a new Mandelbrot Set graph with selected color scheme.
        width = self.width
        height = self.height
        iteration = int(self.iterationEntry.get())

        self.win = graphicsr.GraphWin(self.frame1, self.width, self.height, autoflush=False)
        # Press and drag to get the Julia set with current C value
        self.win.bind("<B1-Motion>", lambda x: self.drawJulia(x))
        # Double click two corners to zoom in
        self.win.bind("<Double-Button-1>", lambda x: self.accumulation(x))
        self.win.setCoords(-1 * self.width/2, -1 * self.height/2, self.width/2, self.height/2)
        self.win.setBackground('black')
        self.win.grid(row = 0, column = 0, rowspan = 35)

        colors = self.colorscheme2(self.col1.get(), self.col2.get(), 16)
        division = self.division.get()
        addition = self.addition.get()
        divisionG = self.divisionG.get()
        additionG = self.additionG.get()

        color = 0
        if self.colorScheme1 == True:
            color = 0
        elif self.colorScheme2 == True:
            color = 1
        elif self.colorScheme3 == True:
            color = 2
        self.abackground = self.bvar.get()

        start = time.clock()
        # If grey Scale is selected, use the division and addition for grey scaling
        if color == 2:
            MandelComputation.cvalue(width, height,self.win, iteration, colors, divisionG, additionG, self.abackground, color)
        else:
            MandelComputation.cvalue(width, height,self.win, iteration, colors, division, addition, self.abackground, color)
        end = time.clock()
        print end - start

    def refine(self):
        # This function refines the inverse julia set into brute forced julia set
        # which is more detailed but requires more computation.
        self.win2 = graphicsr.GraphWin(self.frame2, self.width2, self.height2, autoflush=False)
        self.win2.setCoords(-1 * self.width/2, -1 * self.height/2, self.width/2, self.height/2)
        self.win2.setBackground('black')
        self.win2.grid(row = 0, column = 0, rowspan = 35)
        x = self.dx
        y = self.dy
        c = complex(x/self.width*2.0, y/self.height*2.0)
        # call the brute force function
        MandelComputation.bruteForce(100, self.win2, self.width2, self.height, c.real, c.imag, self.divisionG.get(), self.additionG.get())
    def drawJulia(self, event):
        # This function draws the inverse Julia Set as you click and drag on the Mandelbrot Set window
        # It's fast but less detailed
        self.win2 = graphicsr.GraphWin(self.frame2, self.width2, self.height2, autoflush=False)
        self.win2.setCoords(-1 * self.width/2, -1 * self.height/2, self.width/2, self.height/2)
        self.win2.setBackground('black')
        self.win2.grid(row = 0, column = 0, rowspan = 35)
        self.dx = event.x - 200.0
        self.dy = -1 * event.y + 200.0
        c = complex(self.dx/self.width*2, self.dy/self.height*2)
        # Call the inverse function with necessary arguments
        MandelComputation.inverse(2000, 4.0, c, self.win2)

    ''' The following three functions provide the program the ability to
    switch around three color options by pressing the buttons.
    Each time you select one of the three color options, the tkinter widgets for
    the other will get removed but still stored in memory.  And the tkinter
    widgets for that specific option wil get drawn.
    '''
    # Color smoothing
    def colorChange1(self):
        '''
        :delete whatever widgets of other color option and redraw the widgets for color smoothing
        '''
        if self.colorScheme1:
            self.colorScheme2 = False
            self.colorScheme3 = False
        else:
            if self.colorScheme2:
                self.colorScheme2 = False
                self.colorScheme3 = False
                self.colorScheme1 = True
                self.colorOptionl2.grid_remove()
                self.colLabel1.grid_remove()
                self.col1.grid_remove()
                self.colLabel2.grid_remove()
                self.col2.grid_remove()
            elif self.colorScheme3:
                self.colorScheme2 = False
                self.colorScheme3 = False
                self.colorScheme1 = True
                self.colorOptionl3.grid_remove()
                self.divisionG.grid_remove()
                self.additionG.grid_remove()
                self.divisionGLabel.grid_remove()
                self.additionGLabel.grid_remove()

            self.addLabel.grid(row = 2, column = 1, columnspan = 3)
            self.division.grid(row = 3, column = 0, columnspan = 5)
            self.divLabel.grid(row = 4, column = 1, columnspan = 3)
            self.addition.grid(row = 5, column = 0, columnspan = 5)
            self.BackCheck.grid(row = 6, column = 0, columnspan = 4)
            self.colorOptionl1.grid(row = 1, column = 1, columnspan = 3)
    # Two colors' transformation
    def colorChange2(self):
        '''
        :delete whatever widgets of other color option and redraw the widgets for color transition
        '''
        if self.colorScheme2:
            self.colorScheme1 = False
            self.colorScheme3 = False
        else:
            if self.colorScheme1:
                self.colorScheme1 = False
                self.colorScheme3 = False
                self.colorScheme2 = True
                self.colorOptionl1.grid_remove()
                self.addLabel.grid_remove()
                self.division.grid_remove()
                self.divLabel.grid_remove()
                self.addition.grid_remove()
                self.BackCheck.grid_remove()
            elif self.colorScheme3:
                self.colorScheme1 = False
                self.colorScheme3 = False
                self.colorScheme2 = True
                self.colorOptionl3.grid_remove()
                self.divisionG.grid_remove()
                self.additionG.grid_remove()
                self.divisionGLabel.grid_remove()
                self.additionGLabel.grid_remove()


            self.colLabel1.grid(row = 1, column = 0)
            self.col1.grid(row = 2, column = 0)
            self.colLabel2.grid(row = 3, column = 0)
            self.col2.grid(row = 4, column = 0)
            self.colorOptionl2.grid(row = 0, column = 0)
    # Grey Scale
    def colorChange3(self):
        '''
        :delete whatever widgets of other color option and redraw the widgets for grey scale
        '''
        if self.colorScheme3:
            self.colorScheme1 = False
            self.colorScheme2 = False
        elif not self.colorScheme3:
            if self.colorScheme1:
                self.colorScheme1 = False
                self.colorScheme2 = False
                self.colorScheme3 = True
                self.colorOptionl1.grid_remove()
                self.addLabel.grid_remove()
                self.division.grid_remove()
                self.divLabel.grid_remove()
                self.addition.grid_remove()
                self.BackCheck.grid_remove()
            elif self.colorScheme2:
                self.colorScheme1 = False
                self.colorScheme2 = False
                self.colorScheme3 = True
                self.colorOptionl2.grid_remove()
                self.colLabel1.grid_remove()
                self.col1.grid_remove()
                self.colLabel2.grid_remove()
                self.col2.grid_remove()
            self.colorOptionl3.grid(row = 0, column = 0)
            self.divisionGLabel.grid(row = 1, column =0)
            self.divisionG.grid(row = 2, column = 0)
            self.additionGLabel.grid(row = 3, column = 0)
            self.additionG.grid(row = 4, column = 0)

    def save(self):
        # It's too complicated to install all the libraries necessary
        # to convert eps to jpg or png.  So I just put it in eps format.
        # But I kept the code in comments.
        self.win.postscript(file = "MandelbrotImage.eps")

        '''
        # Have to install 'imagemagick' and 'wand' in order to do the following

        from wand.image import Image
        with Image(filename="MandelbrotImage.eps") as img:
            img.format = 'jpg'
            img.save(filename = "MandelbrotImage.jpg")
        '''


    def make_palette(self):  
        '''a nice color scheme that is not implemented in the gui'''
        '''''sample coloring scheme for the fractal - feel free to experiment'''  
        colours = []  
      
        for i in range(0, 25):  
            colours.append('#%02x%02x%02x' % (i*10, i*8, 50 + i*8))  
        for i in range(25, 5, -1):  
            colours.append('#%02x%02x%02x' % (50 + i*8, 150+i*2,  i*10))  
        for i in range(10, 2, -1):  
            colours.append('#00%02x30' % (i*15))  
        return colours  
    def colorscheme2(self, color1, color2, num):
        '''
        :param color1: a color in hexdecimal string
        :param color2: another color in hexdecimal string
        :param num: the number of colors desired to make the transition between those two colors inputed
        :return: a list of colors
        '''
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
    def accumulation(self, event):
        # This function serve for the zoom in utility.
        # It detects double-clicks and once there are two double-clicks,
        # It calls the zoom in function with necessary arguments
        x = event.x - 200
        y = -1 * event.y + 200




        self.clicksCount += 1
        self.clicks.append(graphicsr.Point(x, y))
        if self.clicksCount == 2:
            win = graphicsr.GraphWin(self.frame1, self.width, self.height, autoflush=False)
            win.setBackground('black')
            win.bind("<B1-Motion>", lambda x: self.drawJulia(x))
            win.bind("<Double-Button-1>", lambda x: self.accumulation(x))
            win.setCoords(-1 * self.width/2, -1 * self.height/2, self.width/2, self.height/2)
            win.grid(row = 0, column = 0, rowspan = 35)
            color = 0
            if self.colorScheme1 == True:
                color = 0
            elif self.colorScheme2 == True:
                color = 1
            elif self.colorScheme3 == True:
                color = 2
            self.abackground = self.bvar.get()
            colors = self.colorscheme2(self.col1.get(), self.col2.get(), 16)
            width = self.width
            height = self.height
            self.win, self.ox1, self.ox2, self.oy1, self.oy2 = MandelComputation.zoomin(self.ox1, self.ox2, self.oy1, self.oy2, width, height, 100, self.frame1, self.division.get(), self.addition.get(), win, self.abackground,  colors, color, self.clicks[0], self.clicks[1])
            self.clicks = []
            self.clicksCount = 0
    def help(self):
        '''
        :return:a graphwin contains the readme.txt
        '''
        q = graphics.GraphWin("Help", width = 600, height = 650)
        q.setCoords(0, 0, 40, 46)
        try:
            file = open('Readme.txt', 'r')
            counter = 46
            for i in file.readlines():
                counter -= 1
                p = graphics.Point(20, counter)
                t = graphics.Text(p, i)
                t.draw(q)
        except IOError:
            text = graphics.Text(graphics.Point(20, 23), "Please to the Readme.txt in the same directory")
            text.draw(q)






def main():
    root = tk.Tk()
    root.title("Mandlebrot")
    root.geometry = ("1000*600")
    # necessary in order to have a menu bar
    menubar = tk.Menu(root)
    newapp = Great(root, menubar)
    root.config(menu=menubar)
    root.mainloop()
    


if __name__ == "__main__":
    cProfile.run("main()", "Profile.prof")
    s = pstats.Stats("Profile.prof")
    s.strip_dirs().sort_stats("time").print_stats(10)
