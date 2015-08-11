# haply-demo
A haptic demo for X-1 demo day, built using Python, Kivy, Cython, and C++. 


### Useful notes: 
- To build cython file: python setup.py build_ext --inplace
- this creates a python .so module file that you can then import in python
	import hello
- don't name .pyx file same as cpp file - a new cpp file will be generated based on pyx one 
- in pyx file should be redefining all variables and functions from C++ header, using:
	- cdef extern from "cpp_module.h": 

### To do: 
- mockups 