
def encrypt(data, key):
    data_len = len(data)
    key_len = len(key)
    new_key = key * (data_len // key_len) + key[0:(data_len % key_len)]
    new_data = b''
    for i in range(0,data_len):
        new_data += ((data[i] ^ new_key[i])&0xff).to_bytes(length=1, byteorder='big', signed=False)
    return new_data


