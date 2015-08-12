# haply-demo
A haptic demo for X-1 demo day, built using Python, Kivy, Cython, and C++. 


### Useful notes: 
TO BUILD ZEROMQ

Update pkg-config if necessary: 
curl http://pkgconfig.freedesktop.org/releases/pkg-config-0.28.tar.gz -o pkgconfig.tgz
tar -zxf pkgconfig.tgz && cd pkg-config-0.28
./configure --with-internal-glib && make install

Install automake:
brew install automake 	# Allows autogen.sh to properly generate the configuration file 

Install libtool:
brew install libtool 	# Prepends a g - glibtool - which allows the autogen.sh file to use libtoolize command

Install libsodium (encryption/password salting and hashing lib):
git clone git@github.com:jedisct1/libsodium.git
bash autogen.sh 	# creates configuration 
./configure			# creates makefile 
make 				# build C files 
make install 		# install on system

Download zeromq, and install:
./configure		 	# Creates makefile out of makefile.am and makefile.in
make 
make install 

TO COMPILE/RUN C++ ZEROMQ FILES 
g++ -I '/usr/local/include' -L /usr/local/lib -lzmq hello_server.cpp 	# link to headers and cpp files
# also need to make sure it's "zmq.hpp" instead of <zmq.hpp> 

g++ -I '/usr/local/include' -L /usr/local/lib -lzmq hello_server.cpp -o helloserver
g++ -I '/usr/local/include' -L /usr/local/lib -lzmq hello_client.cpp -o helloclient

C++ client/server
./helloserver
./helloclient


C++ server/python client
./helloserver
python hello_client.py 

CYTHON 
- To build cython file: python setup.py build_ext --inplace
- this creates a python .so module file that you can then import in python
	import hello
- don't name .pyx file same as cpp file - a new cpp file will be generated based on pyx one 
- in pyx file should be redefining all variables and functions from C++ header, using:
	- cdef extern from "cpp_module.h": 

### To do: 
- mockups 
- vectors instead of arrays