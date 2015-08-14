'''
  TCP server. Sends position information and receives client-side information. 
'''

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

# Wait for the client to be ready 

while True:
    #  Wait for a shape to be added 
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'
    #time.sleep(1)

    #  Send reply back to client
    socket.send_string("0 0")