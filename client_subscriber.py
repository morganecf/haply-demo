'''
  TCP client. Connects to tcp://localhost:5555
'''

import zmq
import time

# The container for all clients in this process
context = zmq.Context()

print "Connecting to server..."

# Client must subscribe to a publisher 
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")

# Set the subscription - updates need to match the pos subscription
socket.setsockopt_string(zmq.SUBSCRIBE, u"pos")

# Wait for position information
while True:
    position = socket.recv_string()
    print "Received position %s" % position
    time.sleep(.01)