#!/usr/bin/env python3

import socket
import time, threading
from util import *

CLIENT_HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
CLIENT_PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
SERVER_HOST = '127.0.0.1'  #'183.173.181.79'
SERVER_PORT = 12345
#content = "<html>\r\n<h1>Secret(Fake)</h1>\r\n<p>You're attacked by 2017010650</p>\r\n</html>"
#text = 'HTTP/1.1 200 OK\r\nServer: nginx/1.14.0 (Ubuntu)\r\nDate: Thu, 10 Dec 2020 19:42:56 GMT\r\nContent-Type: text/html\r\nContent-Length: ' + str(len(content)) + '\r\nLast-Modified: Sat, 14 Nov 2020 20:42:45 GMT\r\nConnection: keep-alive\r\nETag: "5fb04145-4a"\r\nAccept-Ranges: bytes\r\n\r\n' + content

USERNAME = b'username'
PASSWORD = b'password'

def conn(c, a):
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
                ss.connect((SERVER_HOST, SERVER_PORT))
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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((CLIENT_HOST, CLIENT_PORT))
    s.listen()
    while True:
        c, a = s.accept()
        t=threading.Thread(target=conn,args=(c,a))  #创建新线程来处理TCP连接
        t.start()
