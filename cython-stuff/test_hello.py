# This does cython compilation the easy way - use this if don't have extra C libraries 
# or a special build setup. Loads pyx files directly upon import w/out having to write a 
# setup.py script. 

import pyximport; pyximport.install()
import hello

# Use the following line so that the compiler can default to a regular 
# py import if the other method fails: 
	# pyximport.install(pyimport = True)
