import socket
from PIL import Image
import numpy as np

host_name=socket.gethostname()
HOST=socket.gethostbyname(host_name)
PORT=8000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)

def generateKey(len_str, key): # len_str = Độ dài key cần tạo(int), key(string) => return key được lặp lại (string)
    key = list(key)
    if len_str == len(key):
        return(key)
    else:
        for i in range(len_str - len(key)):
            key.append(key[i % len(key)])
    return("" . join(key))
     
# TEXT
def cipherText(string, key): # Mã hóa text
    cipher_text = []
    key = generateKey(len(string), key)
    for i in range(len(string)):
        x = (ord(string[i]) + ord(key[i])) % 256
        # x += ord('A')
        cipher_text.append(chr(x))
    return("" . join(cipher_text))

def decryptedText(cipher_text, key): # Giải mã text
    decry_text = []
    key = generateKey(len(cipher_text), key)
    for i in range(len(cipher_text)):
        x = (ord(cipher_text[i]) -
             ord(key[i]) + 256) % 256
        # x += ord('A')
        decry_text.append(chr(x))
    return("" . join(decry_text))


# IMAGE
def encodeImg(img, key):    # img = Array của numpy , key(string) bất kì
    print("Proceed to encode the image...")
    # Tạo key (mảng 3 chiều (int))
    key_num = []
    (h,w,d) = img.shape
    key = generateKey(h*w*d,key)
    for i in range(h*w*d):
        key_num.append(ord(key[i]))
    key_num = np.array(key_num)
    key_num = np.reshape(key_num,(-1,w,d))
    # Mã hóa
    img = (img + key_num) %256
    print("Done")
    return img.astype(np.uint8)
                
def decodeImg(img, key): # img = string, key của encodeImg
    print("Proceed to decode the image...")
    # Tạo key (mảng 3 chiều (int))
    (h,w,d) = img.shape
    key = generateKey(h*w*d,key)
    key_num = []
    for i in range(h*w*d):
        key_num.append(ord(key[i]))
    key_num = np.array(key_num)
    key_num = np.reshape(key_num,(-1,w,d))
    # Giải mã
    img = (img - key_num + 256) %256
    print("Done")
    return img.astype(np.uint8)

def chat():
    print("Chat:")
    try:
        while True:
            msg = input('Client: ')
            s.sendall(bytes(msg, "utf8"))
            if msg == "quit":
                functions()
                break
            data = s.recv(1024)
            print('Server: ', data.decode("utf8"))
    finally:
        s.close()

def sendtext():
    print("Receive file text:")
    print("Nhap duong dan luu file: ")
    path=str(input())
    with open(path,'wb') as f:        #"D:/anhthe/khai.txt"
        print("file opened")
        data=s.recv(1000000)
        f.write(data)
        print("data :", data)
        f.close()
    with open(path, 'r', encoding = 'utf-8') as f:
        #‘rb’	Mở file chế độ đọc cho định dạng nhị phân
        c=f.read()
        print("file text : ",c)
    s.sendall(bytes("ok", "utf8"))
    functions()


def sendImage():
    print("Receive image")
    print("Nhap duong dan luu anh: ")
    path=str(input())
    # D:/anhthe/anhthe.jpg
    with open(path,'wb') as f:
        print("file opened")
        data=s.recv(1000000)
        f.write(data)
        print(data)
        f.close()
    with open(path, 'rb') as f:
        im = Image.open(f)
        im.show()
    s.sendall(bytes("ok", "utf8"))
    functions()

def functions():
    print("Chon cach truyen tin:")
    print("1: Chat")
    print("2: Receive file text")
    print("3: Receive image")
    print("4: End")
    x=int(input())
    if x==1:
        chat()
    elif x==2:
        sendtext()
    elif x==3:
        sendImage()
    else:
        print("END")
        return

def connect():
    print('connecting to %s port ' + str(server_address))
    s.connect(server_address)
    functions()

if __name__ == "__main__":
    connect()