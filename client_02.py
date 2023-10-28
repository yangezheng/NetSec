#!/usr/bin/env python3
import socket
from base64 import b64encode, b64decode

HOST = 'thisisno.valid.hostname'
PORT = 42

username = input("Username (hint: root): ")
password = input("Password (hint: PasswordXX, X=0-9): ")
credentials=username+","+password

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))
sf = s.makefile("rw")  # we use a file abstraction for the sockets

sf.write("{}\n".format(credentials))
sf.flush()

challenge = sf.readline().rstrip('\n')

print("Solve the following equation to prove you are human: ", challenge)
response=input("Solution: ")
sf.write("{}\n".format(response))
sf.flush()

data = sf.readline().rstrip('\n')
print("From Server: `{}'".format(data))

data = sf.readline().rstrip('\n')
print("From Server: received {} bytes".format(len(data)))

data = b64decode(data.encode())

pdf_hdr = b'%PDF-1.5'

if len(data) >= len(pdf_hdr) and data[:len(pdf_hdr)] == pdf_hdr:
    print("Looks like we got a PDF!")
    # TODO write the received data to a file

sf.close()
s.close()
