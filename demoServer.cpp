// TCP server. Binds REP socket to tcp://*:5556 

#include "zmq.hpp"
#include "zhelpers.hpp"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    //  Prepare our context and publisher
    zmq::context_t context(1);
    zmq::socket_t publisher(context, ZMQ_REP);
    publisher.bind("tcp://*:5556");

    // Create the fake walk 
    std::string walk[800];

    int i;
    for (i = 0; i < 800; i++) {
        walk[i] = std::to_string(i) + " " + std::to_string(i);
    }

    i = 0;
    while (true) {
        // Just repeat the walk
        if (i >= 800) i = 0;

        // Send envelope 
        s_sendmore(publisher, "pos");
        s_send(publisher, walk[i]);

        // Synchronize with client 
        usleep(10);

        i++;
    }

    return 0;
}

