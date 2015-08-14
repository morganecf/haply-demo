import zmq
import time
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

path = [(1, 2), (3, 4), (5, 6), (7, 8)]

while True:
    # zipcode = randrange(1, 100000)
    # temperature = randrange(-80, 135)
    # relhumidity = randrange(10, 60)

    # socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))
    time.sleep(0.33)
    if path:
      point = path.pop()
    # Send the current point or last point in the list 
    socket.send_string("%i %i" % (point[0], point[1]))

    print "Sending:", point