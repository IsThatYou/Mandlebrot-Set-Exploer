In order to run this program, cython is required. It provides great speed up with
its c extension butalso brings inconvenience for the users who are using them.
To install Cython:
For Mac users:
1. go to http://cython.org/#download and download the gzip file
2. unzip the gzip
3. go to the directory setup.py of cython folder with the terminal
4. type in the command "arch -32 python setup.py install" without the quotation mark
5. done
For Windows users:
It's a lot more complicated for windows.
First you should go download the zip file and then try the setup.py.
If you encounters errors "unable to find vcvarsall.bat", go to this post:
http://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat?lq=1
------------------------------------------------------------------------------------------
How to use it:

Double-click two corners of the rectangle to select the area that needs zoom in.
Click and drag to draw the Julia set with the c value selected by the point.

Iteration: you can change it to increase the precision of the graph.

Color Option I: The smooth coloring.  It colors the graph with multiple colors and
very smooth transition.  you can change it's smooth value and color value with the
scales.  The mysterious background gives an amazing affect to the graph, try it out!

Color Option II: The graph will become the repentance of two colors you input. Input
the color in hexdecimal. To find some good colors in hex, I suggest this website:
http://nipponcolors.com/#tsuyukusa

Color Option III: It gives an awesome old school effect of grey scaling.Mysterious
background is assumed in this option.

Create: The program will generate a new Mandelbrot set with selected color scheme.

Apply: Instead of generating a new graph, this option provides you the ability to switch
color scheme while staying at the same zoom in level

Refine Julia Set: Ihe programs will refine the inverse Julia set to give it greater details.

Top menu bar:

save mandelbrot: It will save the current window in a '.eps' format at the same directory.

Help: It will open this file in a more artistic way.
