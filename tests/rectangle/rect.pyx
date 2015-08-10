''' Wrapping a C++ class ''' 

# Make the C++ class def for rectangle available 
cdef extern from "Rectangle.h" namespace "shapes":
	# A cython wrapper class 
	cdef cppclass Rectangle: 
		# Attributes and methods for use in Cython
		Rectangle(int, int, int, int) except + 		# this is the constructor 
		int x0, y0, x1, y1
		int getLength()
		int getHeight()
		int getArea()
		void move(int, int)

# Example cython usage of this class
#cdef Rectangle *rec = new Rectangle(1, 2, 3, 4)
#rlen = rec.getLength()
#print rlen
#del rec 

# Python wrapper for cython class 
cdef class PyRectangle:
	cdef Rectangle *thisptr      # hold a C++ instance which we're wrapping
	def __cinit__(self, int x0, int y0, int x1, int y1):
		self.thisptr = new Rectangle(x0, y0, x1, y1)
	def __dealloc__(self):
		del self.thisptr
	def getLength(self):
		return self.thisptr.getLength()
	def getHeight(self):
		return self.thisptr.getHeight()
	def getArea(self):
		return self.thisptr.getArea()
	def move(self, dx, dy):
		self.thisptr.move(dx, dy)

# Use this class the normal pythonic way 

