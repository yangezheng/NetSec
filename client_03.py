#!/usr/bin/env python3
import socket
import time

HOST = 'netsec.net.in.tum.de'
PORT = 20003

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

buf = s.recv(1024)
print(buf.decode())

#  ▲
# ▲ ▲
triforce = " ▲\n▲ ▲"  # Triforce symbol made with upward-pointing triangles

# Encode the Triforce symbol into UTF-8
utf8_encoded = triforce.encode('utf-8')

# TODO you should send your triforce here
print("Start Sending...", flush=True)

for byte in utf8_encoded:
    print("sending byte of: ")
    print(byte)
    s.send(bytes([byte]))  # Sending each byte separately
    time.sleep(1)  # Delay of one second between each byte

# Sleeping for additional time to ensure the server receives the data
time.sleep(3)

sf = s.makefile("rw")
buf = sf.readline().rstrip('\n')
print(buf)

data = sf.readline().rstrip('\n')
print("From Server: received {} bytes".format(len(data)))

print(data)

sf.close()
s.close()
