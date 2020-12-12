#!/usr/bin/env python3

import socket
import time, threading
import argparse
from util import *

USERNAME = b'username'
PASSWORD = b'password'

def conn(c, a, args):
    with c:
        print('Connected by', a)
        while True:
            data = c.recv(1024)
            print(data)
            if not data or len(data) == 0:
                print("break1")
                break
                #conn.sendall(str.encode(text))
            if 'CONNECT' in str(data):
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
                ss.connect((args.server_host, args.server_port))
                ss.settimeout(3)
                send_msg(ss, data, USERNAME, PASSWORD)
                while True:
                    try:
                        sdata = recv_msg(ss, from_client=False)
                    except socket.timeout:
                        break
                    #print(sdata)
                    if not sdata:
                        print("break2")
                        break
                    c.sendall(sdata)
        c.close()
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--client_host', type=str, default='127.0.0.1', help='Standard loopback interface address (localhost)')
    parser.add_argument('--client_port', type=int, default=65432, help='Port to listen on (non-privileged ports are > 1023)')
    parser.add_argument('--server_host', type=str, default='127.0.0.1', help='server host')
    parser.add_argument('--server_port', type=int, default=12345, help='server port')

    args = parser.parse_args()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((args.client_host, args.client_port))
        s.listen()
        while True:
            c, a = s.accept()
            t=threading.Thread(target=conn,args=(c,a,args))  #创建新线程来处理TCP连接
            t.start()
