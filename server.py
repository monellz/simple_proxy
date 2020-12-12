import socket
import requests
import multiprocessing
import re
import urllib
import argparse
from util import *

user_data = {
  b'username': b'password'
}

def user_available(username, password):
  return username in user_data.keys() and user_data[username] == password

def work(cnn):
  while True:
    try:
      res, username, password = recv_msg(cnn)
      if not res:
        break
      if not user_available(username, password):
        print("user not available:", username, password)
        break
    except ConnectionResetError:
      break

    rs_url = re.findall(r"GET ([\w:/\.]+)", str(res))
    if len(rs_url) == 0:
      break
    print(res)
    netloc = urllib.parse.urlparse(rs_url[0]).netloc
    print("rs_url: ", rs_url)
    print("netloc: ", netloc)
    print("socket: ", cnn)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rs:
      rs.connect((netloc, 80))
      rs.settimeout(3)
      rs.sendall(res)
      while True:
        try:
          data = rs.recv(1024)
        except socket.timeout:
          print("timeout rs_url: ", rs_url)
          break

        if not data:
          print("remote server send done")
          break
        send_msg(cnn, data, b'', b'')
  cnn.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--server_port', type=int, default=12345, help='server port')

  args = parser.parse_args()

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('0.0.0.0', args.server_port))
  s.listen(5)
  while True:
    try:
      print("start listen from main")
      cnn, addr = s.accept()
      print("get connection from addr: ", addr)
      m = multiprocessing.Process(target=work, args=(cnn,))
      m.daemon = True  # daemon True设置为守护即主死子死.
      m.start()  # 开启一个子进程, func中的while 来接受cnn后续内容.
    except ConnectionResetError:
      pass
    except Exception as e:
      print(e)