# Test the cython vs. python fibonacci methods 

import time 
import pyximport; pyximport.install()
import fibC
import fibP 

n = 10000000

fc = []
fp = []

# Time the cython version 
start = time.time()
for x in range(n):
	fc.extend(list(fibC.fib(x)))

print 'Cython:', time.time() - start

# Time the python version
start = time.time()
for x in range(n):
	fp.extend(list(fibP.fib(x)))

print 'Python:', time.time() - start



''' 
Results 

x = 5000
Cython: 0.0107140541077
Python: 0.0141589641571

x = 10000
Cython: 0.0224289894104
Python: 0.0289301872253

x = 100000
Cython: 0.277990102768
Python: 0.381635904312

x = 1000000
Cython: 3.05309605598
Python: 4.25705981255

x = 10000000
Cython: 40.7367110252
Python: 54.8656468391

'''

