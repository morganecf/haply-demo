'''
  TCP server. Binds a response socket to tcp://*:5555.
'''

import zmq
import time 
import math
import random

# The uniform probability of picking an action for the 
# random walk, since there are 9 options
_rp = 1.0 / 9.0     # 0.1111

# The possible actions. Walker can take 9 actions
# left, right, bottom, stay put, etc. 
_actions = [(0, 0), (0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)]

_action_labels = ['stay', 'up', 'right', 'up-right', 'left', 'down', 'down-left', 'up-left', 'bottom-right']

# Return a random path of length n through the grid
def random_walk(n):
  # Start off at 0,0
  path = [[0, 0]]
  directions = ['start']

  for i in range(n):
    # Pick an action w/ uniform prob
    r = random.random()
    a = int(math.floor(r / _rp))  

    # Perform this action and add to path list 
    path.append([path[i][0] + _actions[a][0], path[i][1] + _actions[a][1]])
    directions.append(_action_labels[a])

  return path, directions 

# Return a biased random path of length n through the grid
def biased_random_walk(n):
  # Start off at 0,0
  path = [[0, 0]]

  # Will keep track of counts of each action taken 
  # to create a biased random walk 
  action_counts = [0]*9

  for i in range(n):
    # Pick an action w/ uniform prob
    r = random.random()
    a = math.floor(r / _rp)

    # Increase the count of this action 
    action_counts[a] += 1

    # Perform this action 
    path[i][0] += _actions[a][0]
    path[i][1] += _actions[a][1]

# Return a straight diagonal walk across the grid 
def diagonal_walk(n): return zip(range(n), range(n))

# Establish context and connect to socket 
context = zmq.Context()

# Publishes information to clientss
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

# Create a random path 
path = diagonal_walk(400)

# Send positions from path to the client 
while True:
    # Synchronize with client 
    time.sleep(.01)

    if path:
      point = path.pop()

    # Send the current point or last point in the list 
    socket.send_string("%s %i %i" % (u"pos", point[0], point[1]))

    print point

