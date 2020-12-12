import struct


def encrypt(data, key):
    key = key * (len(data) // len(key) + 1)
    key = key[:len(data)]
    int_data = int.from_bytes(data, byteorder='big', signed=False)
    int_key = int.from_bytes(key, byteorder='big', signed=False)
    int_enc = int_data ^ int_key
    return int_enc.to_bytes(len(data), byteorder='big', signed=False)

KEY = b"thisisakeybutitseemstooshortsoidecidedtomakeitlonger23re8fwohnu4rwqjfekaafuh4qfnwjkuh4t735ygihug983yygfbiwuhg9578y3fu3bhdiu3hf9grhe6rh2t+e1therym;'.,[]o.,u]y[um.rtrgp2[,f198e4j6*9/-*0+-=90lk5jyh21g0v fb kjedmiujkrje57k4588/kkur*j-y6h5g34fwe\r4--qe1sdfsgs\nsdq*-4f*-4-*v2c25-cg254t124b-12434*-t2134/n-*123/4b-5*232/845-48223*4-55v22*-4552-34*55213b-*213b545*-b213-45*b12-34*5b28*-4sdvuasidnvjasdvbasdhvbSDBVASFJBRHERIUHGIHUGQUOIHG98`90U2`U`RFGR;;W'E.RB[]BP.R,OMNT[PELRNT[];.RT,NPOJERTH[PKRMGNIWOERPBJOMKNTRPOK[PE]TNM*.*/--*748EYR4N84YTTMT-UI,8O.189.O8-,YTMNYTBRVDVFBGNYHarbbBUYBhbjhbUBCjbjhBJHBjkbj19+5C6551616a5161s6b1FBSBNT45IHONG b651b65sfbswnNWRLWNW+hao049gibnok'sfvsbgww-p[;..ll-090-0p;.56h,5ph;eve;.rnm,.*p8/*-.'=][p;lkjthyui,ol;908l97k86j*-yhr8t9er5 SBTHEJ5EYRNbs*n-egs849bdt1bBQNiBgfThNjC59cCIc3c9516516516516bsfdbsfbsfnomqmbrq8965b4re+v954ab+*4b499r4ba+sf4b+9fb4a+3q8432543656940-g-b=[;.;,lonk0o-b ll-po,w05h-o6jp7k8u\ramij09-0kromph5kmeltnbf\noiajsd9poibreoh54OUGY6F8G798HGJ43I4NTOU2FBIEYUCSH8iabuoijeoph9n0yhi fngpbijehtinrymmut,i+y8jmnbB9N9YM857K*748JYRN4T+B9RV8*B+849Bsbn48+t*7m948snbr/h-5j*6m9yjr5n4b8g+*8h-/7ge8v4asc4v8b+*nt849jy84+ntebwvcAABQNTI6OMTEB903H58NGOIWEVb59h5-e8n*t+48b95BREN57R489 4+989b4h74+94w5h48nt+eh8*58e4rv'5684+8*-95+bniwuj0983h5bietunym51yn84+t*9g59q+5btnwNQT84+99TR+GSN1YEM84Y+9N5TBRS+RBTNnye8l9o;p9ololp;[';p.l,munyqNYUEYRNSTBGDTNY];KNTWEMRPOKGIMOBLKV MVNJBNSDFBe54*+39-4*8+h*53*h+84br95+1b+bwsdNTWnawKMYPONTBRVweh43g9+45*-748+9e45b4nt96em57k488+k6746j569htbetep;'.[v]\';.;[B]R;TNM][7UM[;\[MT].;Y,NT[BPB.E;N;YRTE.BR]R[B.][R.B].B[]SDF.+5B+9SD5+49M,+.;94/++GF4WFD;908l;st;n.+9/2+9/2+9fgl,f9iadfp[-0LHN;'F,.+9/P+95.;'.sdp-04-[j.mru9+26o9+o2.+59rpoWT95N+E4YYI;[][.[.+6t5k+93u5+tu9iu5nfv"

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