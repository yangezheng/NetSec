#!/usr/bin/env python3

import socket

# Fill in the right target here
HOST = 'thisisno.valid.hostname'    # TODO
PORT = 42                           # TODO

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
sf = s.makefile("rw")  # we use a file abstraction for the sockets

def read(sf):
    data = sf.readline().rstrip('\n')
    print("From Server: `{}'".format(data))

def write(sf):
    data = input("Your Answer: ")
    sf.write("{}\n".format(data))
    sf.flush()

# ToDo: implement communication with server here, using the template functions above

sf.close()
s.close()
