from setuptools import setup 
from Cython.Build import cythonize 

# Tell cython we are using C++
setup(ext_modules = cythonize('hello.pyx'))