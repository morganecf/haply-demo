import sys
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5556")

# Subscribe to zipcode, default is NYC, 10001
#zip_filter = "10001"

# Python 2 - ascii bytes to unicode str
# if isinstance(zip_filter, bytes):
#     zip_filter = zip_filter.decode('ascii')
socket.setsockopt_string(zmq.SUBSCRIBE, u"10001")

# Process 5 updates
#for update_nbr in range(5):
while True:
    string = socket.recv_string()
    print string

print("Done")