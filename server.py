import socket
import requests
import multiprocessing
import re
import urllib

def work(cnn):
  while True:
    try:
      res = cnn.recv(1024)
    except ConnectionResetError:
      break

    if not res:
      break

    rs_url = re.findall(r"GET ([\w:/\.]+)", str(res))
    if len(rs_url) == 0:
      break

    netloc = urllib.parse.urlparse(rs_url[0]).netloc
    print("rs_url: ", rs_url)
    print("netloc: ", netloc)
    print("socket: ", cnn)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as rs:
      rs.connect((netloc, 80))
      rs.settimeout(2)
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
        cnn.sendall(data)
  cnn.close()

if __name__ == '__main__':
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('0.0.0.0', 12345))
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