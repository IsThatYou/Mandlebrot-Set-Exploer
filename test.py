__author__ = 'Wangj1'
from distutils.core import setup, Extension
from Cython.Distutils import build_ext


setup (name = "Escape",
 version = "0.1",

 ext_modules = [Extension('escapecy',
 ['MandelComputation.pyx'])],
 cmdclass = {'build_ext': build_ext}
 )




