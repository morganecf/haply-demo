''' Wrapping the C++ ball class ''' 

# The Cython wrapper for the C++ class 
cdef extern from "Ball.h" namespace "shapes":
	cdef cppclass Ball: 
		Ball(int, int, float, float) except + 		# the constructor 
		int cx, cy
		float r, v, m
		int *p
		int *getPos()
		float getVel()
		float getMass()
		void accelerate()
		void move(int, int)

# Example cython usage of this class
# cdef Ball *ball = new Ball(50, 50, 1.0, 40.0)
# radius = ball.getRadius()
# del ball 

# Python wrapper for cython class - use it the normal pythonic way 
cdef class pyBall:
	# Hold a pointer to the C++ ball instance which we're wrapping
	cdef Ball *bp    

	# Gets called before __init__
	def __cinit__(self, int cx, int cy, float r, float m):
		self.bp = new Ball(cx, cy, r, m)

	# Destructor
	def __dealloc__(self):
		del self.bp

	def getPos(self): 
		pos = self.bp.getPos()
		return [pos[0], pos[1]]

	def getVel(self): return self.bp.getVel()
	def getMass(self): return self.bp.getMass()

	def accelerate(self): return self.bp.accelerate()
	def move(self, dx, dy): return self.bp.move(dx, dy)

