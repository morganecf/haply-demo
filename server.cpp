// TCP server. Binds REP socket to tcp://*:5555 and serves positional information.

#include "zmq.hpp"
#include "zhelpers.hpp"
#include <stdio.h>
#include <stdlib.h>

//#define sleep(n)    Sleep(n)

int main() {
    //  Prepare our context and publisher
    zmq::context_t context(1);
    zmq::socket_t publisher(context, ZMQ_PUB);
    publisher.bind("tcp://*:5556");

    while (true) {
        // Send envelope 
        s_sendmore(publisher, "pos");
        s_send(publisher, "0 0");

        // Synchronize with client 
        //sleep(.01);
    }

    return 0;
}