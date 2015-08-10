
# Cython wrapper of C++ class 
cdef extern from "cpp_test.h":
	cdef cppclass Test:
		Test()
		Test(int test1)
		int test1
		int returnFive()
		Test add "operator+"(Test Other)		# Can rename C++ functions 
		Test sub "operator-"(Test Other)

# Python wrapper of Cython class 
cdef class pyTest:
	cdef Test* thisptr		# Holds the C++ instance - pointer to the above class/point of access of C++ functions

	# This gets called before __init__ 
	def __cinit__(self, int test1):
		self.thisptr = new Test(test1)

	def __dealloc__(self):
		del self.thisptr

	def __add__(pyTest left, pyTest other):
		cdef Test t = left.thisptr.add(other.thisptr[0])
		cdef pyTest tt = pyTest(t.test1)
		return tt

	def __sub__(pyTest left, pyTest other):
		cdef Test t = left.thisptr.sub(other.thisptr[0])
		cdef pyTest tt = pyTest(t.test1)

	def __repr__(self):
		return "pyTest[%s]" % self.thisptr.test1

	def returnFive(self):
		# Not everything has to be redefined - still calls returnFour 
		# even though we haven't defined it 
		return self.thisptr.returnFive()

	# Can add extra functionality to the python class that 
	# isn't defined in C++ one 
	def printMe(self):
		print "Hello World!"


