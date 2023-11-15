#!/usr/bin/env python3

import argparse
import asyncio
import logging
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64encode
import subprocess

from utils import log_error, read_line_safe


log = logging.getLogger(__name__)
clients = {}  # task -> (reader, writer)

stored_data = None    # binary
encryption_key = None
client_count = 0


def accept_client(client_reader, client_writer, loop):
    global client_count

    client_id = client_count
    client_count += 1
    task = loop.create_task(handle_client(client_reader,
                                          client_writer,
                                          client_id))
    clients[task] = (client_reader, client_writer)

    def client_done(task):
        del clients[task]
        client_writer.close()
        log.info("[%d] connection closed" % client_id)

    task.add_done_callback(client_done)


async def handle_client(client_reader, client_writer, client_id):
    try:
        remote = client_writer.get_extra_info('peername')
        if remote is None:
            log.error("Could not get ip of client")
            return
        
        remote = "%s:%s" % (remote[0], remote[1])
        log.info("[%d] new connection from: %s" % (client_id, remote))
    except Exception as e:
        log.exception("get peername failed")
        return

    try:
        client_writer.write("Welcome to Bob's data storage\n".encode())
        await client_writer.drain()

        cmd = await read_line_safe(client_reader)

        if cmd is None:
            client_writer.write("No command received\n".encode())
            await client_writer.drain()
            return

        def encrypt(plaintext):
            iv = Random.new().read(AES.block_size)

            #add padding
            if len(plaintext) % 16 != 0:
                plaintext += b'_' * (16 - len(plaintext) % 16)

            cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(plaintext)

            return b64encode(iv) + b"," + b64encode(ciphertext) + b"\n"

        def no_transform(plaintext):
            return b64encode(plaintext) + b"\n"

        commands = {"SEND ENCRYPTED DATA": encrypt,
                    "SEND DATA": no_transform}

        if len(cmd) != len("SEND ENCRYPTED DATA"):
            client_writer.write("Bob does not allow commands of length {}\n".format(len(cmd)).encode())
            await client_writer.drain()
            return

        cmd = cmd.replace('_', '')

        if cmd not in commands.keys():
            client_writer.write("Unknown command `{}'. Available commands are {}\n".format(cmd, str(commands.keys())).encode())
            await client_writer.drain()
            return

        transform = commands[cmd]
        message = transform(subprocess.check_output("flag"))
        client_writer.write("Sending data\n".encode())
        client_writer.write(message)
        await client_writer.drain()

    except Exception as e:
        log_error(e, client_writer)


def main():
    global encryption_key

    cmd = argparse.ArgumentParser()
    cmd.add_argument("-p", "--port", type=int, default=20005)
    args = cmd.parse_args()

    encryption_key = Random.new().read(AES.block_size)

    # start server
    loop = asyncio.get_event_loop()
    f = asyncio.start_server(lambda r, w: accept_client(r, w, loop),
                             host=None, port=args.port)
    log.info("starting to listen on port %d..." % args.port)
    loop.run_until_complete(f)
    log.info("server waiting for connections...")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s "
                               "[%(module)s:%(lineno)d] %(message)s")
    main()
