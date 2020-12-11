import struct


def encrypt(data, key):
    key = key * (len(data) // len(key) + 1)
    key = key[:len(data)]
    int_data = int.from_bytes(data, byteorder='big', signed=False)
    int_key = int.from_bytes(key, byteorder='big', signed=False)
    int_enc = int_data ^ int_key
    return int_enc.to_bytes(len(data), byteorder='big', signed=False)

KEY = b"thisisakey"

def send_msg(sock, data, username, password, key=KEY):
  # 发送 len(KEY(data+username+password)) KEY(data+username+password)
  data = data + username + password
  encrypted_data = encrypt(data, key)
  len_bytes = struct.pack('!I', len(encrypted_data))
  sock.sendall(len_bytes)
  sock.sendall(encrypted_data)

def recv_msg(sock, key=KEY, from_client=True):
  len_bytes = sock.recv(4)
  if len(len_bytes) != 4:
    if from_client: return None, None, None
    else: return None
  data_len = struct.unpack('!I', len_bytes)[0]
  encrypted_data = sock.recv(data_len)
  data = encrypt(encrypted_data, key)
  if from_client: return data[:-16], data[-16:-8], data[-8:]
  else: return data