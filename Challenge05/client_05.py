#!/usr/bin/env python3
import socket
from base64 import b64encode, b64decode


HOST = 'netsec.net.in.tum.de'    # TODO
PORT = 20005                     # TODO


def main():
    # create socket and connect to bob
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Our protocol is line-based. Each message should end with an '\n'. Otherwise, it may result in errors!
    # If your script is stuck (i.e the buffer is not flushed), you probably forgot the newline.

    s.connect((HOST, PORT))
    sf = s.makefile("rw")  # we use a file abstraction for the sockets

    banner = sf.readline().rstrip('\n')
    print("From Bob: `{}'".format(banner)) # you should see the newline at the end printed

    # "SEND ENCRYPTED DATA"
    sf.write("SEND __________DATA\n")
    sf.flush()

    data = sf.readline().rstrip('\n')
    print("From Bob: `{}'".format(data))

    data = sf.readline().rstrip('\n')
    print("From Server: received {} bytes".format(len(data)))

    if ',' in data:
        # IV,ENCRYPTED DATA
        print("Data seems to be encrypted")
        return
    
    de_data = b64decode(data)
    print(de_data)

    sf.close()
    s.close()

main()


