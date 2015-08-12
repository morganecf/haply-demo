from setuptools import setup 
from setuptools.extension import Extension
from Cython.Build import cythonize 

setup(ext_modules = cythonize(Extension('ball', sources=['pyball.pyx', 'ball.cpp'], language='c++')))