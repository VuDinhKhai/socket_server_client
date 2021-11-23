import socket
from PIL import Image
import numpy as np
import cv2
import os

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

def chat(key):
    print("Chat:")
    try:
        while True:
            msg = input('Client: ')
            ci_msg=cipherText(msg,key)
            s.sendall(bytes(ci_msg, "utf8"))
            if msg == "quit":
                functions(key)
                break
            data = s.recv(1024)
            str_data=data.decode("utf8")
            de_data=decryptedText(str_data,key)
            print('Server: ', de_data)
    finally:
        s.close()

def Recvtext(key):
    print("Receive file text:")
    print("Nhap duong dan luu file: ")
    path=str(input())
    with open(path,'wb') as f:        #"D:/anhthe/khai.txt"
        print("file opened")
        data=s.recv(100000000)
        f.write(data)
        print("data :", data)
        f.close()
    with open(path, 'r', encoding = 'utf-8') as f:
        #‘rb’	Mở file chế độ đọc cho định dạng nhị phân
        c=f.read()
        print("file text : ",c)
        #l=decryptedText(c,key)
        #print("file text : ",l)

    s.sendall(bytes("ok", "utf8"))
    functions(key)


def RecvImage(key):
    print("Receive image")
    print("Nhap duong dan luu anh: ")
    path=str(input())
    # D:/anhthe/Doremon.jpg
    with open(path,'wb') as f:
        print("file opened")
        data=s.recv(1000000)
        f.write(data)
        #print(data)
        f.close()
    pathnew=deImage_k(path,key)
    print("Anh nhan duoc: " ,pathnew)
    s.sendall(bytes("ok", "utf8"))
    deletepath(path)
    functions(key)

def deImage_k(path,key):
    file_img=cv2.imread(path)
    img=np.array(file_img)
    de=decodeImg(img,key)
    de_image=Save_deImage(path,de)
    return de_image

def Save_deImage(path,cip):
    tail = "." + path.split(".")[-1] # Lấy ra đuôi của file ảnh ban đầu VD: "C:/Kai.png" -> ".png"
    path_save = "./"  # ./ là thư mục đang chạy này
    name = "encode_Img" # Tên (Không cần đuôi)
    cv2.imwrite(path_save + name + tail, cip) #  Lưu file
    pathnew=path_save + name + tail
    return pathnew

def deletepath(path):
    try: 
        os.remove(path)
    except: pass
def functions(key):
    print("Chon cach truyen tin:")
    print("1: Chat")
    print("2: Receive file text")
    print("3: Receive image")
    print("4: End")
    x=int(input())
    if x==1:
        chat(key)
    elif x==2:
        Recvtext(key)
    elif x==3:
        RecvImage(key)
    else:
        print("END")
        return

def connect():
    print("Nhap key: ")
    key=str(input())
    print('connecting to %s port ' + str(server_address))
    s.connect(server_address)
    print("Nhap key: ")
    key=str(input())
    data = s.recv(1024)
    str_data=data.decode("utf8")
    if str_data!=key:
        s.disconnet(server_address)
    functions(key)

if __name__ == "__main__":
    connect()
    # path=deImage_k("D:/anhthe/Doremon.jpg","key:VuxDDinhkhaideptraisieucapvippro%%%%%%%%%%%%$$$$$$$$$###########")
    # with open(path, 'rb') as f:
    #     im = Image.open(f)
    #     im.show()
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()