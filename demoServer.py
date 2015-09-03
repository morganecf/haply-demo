'''
  TCP server. Receives client-side information and sends positional information back. 
  Haptics are enabled when the sever receives the 'hapify' request from the client. It 
  then receives all the shapes and their positions on the canvas, and initializes these 
  in the physics simulation. It then sends positional information back to the client.   

  When it receives a dehapify request, stops the simulation. 
'''

import zmq
import time
import random

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")


# A sample simulation -- user moves a few of the shapes 
# up and over by 5px every second, for ten seconds. 
# This is where we would listen for input from the haptic device 
def simulation(shapestr):
	# Parse the shape information 
	shapes = []
	for s in shapestr.split('\t'):
		s = s.split(',')
		shape = [s[0], float(s[1]), float(s[2]), s[3]]
		shapes.append(shape)

	for x in range(10):
		info = ''
		for shape in shapes:
			shape[1] = str(float(shape[1]) + 5)
			shape[2] = str(float(shape[2]) + 5)
			info += '\t' + ','.join(shape)

		socket.send_string(info)
		print socket.recv()
		time.sleep(1)


while True:
    # Wait for the hapify/dehapify request 
    message = socket.recv()

    if message == 'hapify':
    	# Request shapes 
    	socket.send_string("shape-req")
    	# Receive shapes 
    	shapes = socket.recv()
    	# Run simulation
    	simulation(shapes)
    	# Send response
    	socket.send_string("simulation done")

    else:
	    # Send reply back to client
	    socket.send_string('dehapifying')


