from setuptools import setup 
from setuptools.extension import Extension
from Cython.Build import cythonize 

# Tell cython we are using C++
setup(ext_modules = cythonize(Extension('rect', sources=['rect.pyx', 'Rectangle.cpp'], language='c++')))