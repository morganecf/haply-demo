from setuptools import setup
from setuptools.extension import Extension

#from Cython.Disutils import build_ext 
from Cython.Build import cythonize 

# Cython.Disutils build_ext method - didn't work because can't find Disutils module
# setup(
# 	name = 'Demos',
# 	ext_modules = [ 
# 		Extension("test", 
# 			sources = ["test.pyx", "cpp_test.cpp"], # Can link against a C++ library instead of including the source
# 			language = "c++"
#         ),
# 	],
# 	cmdclass = {'build_ext': build_ext},
# )

# Cython.Build cythonize methods
#setup(ext_modules = cythonize('test.pyx', sources=['cpp_test.cpp'], language='c++'))
setup(ext_modules = cythonize(Extension("test", sources=['test.pyx', 'cpp_test.cpp'], language='c++')))