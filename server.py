import socket
import threading
import numpy as np
import cv2
import os 

host_name=socket.gethostname()
HOST=socket.gethostbyname(host_name)
PORT=8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

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

def deImage_k(path,key):
    file_img=cv2.imread(path)
    img=np.array(file_img)

    cip=encodeImg(img,key)
    return savepath(path,cip)

def deletepath(path):
    try: 
        os.remove(path)
    except: pass

def savepath(path,cip):
    tail = "." + path.split(".")[-1] # Lấy ra đuôi của file ảnh ban đầu VD: "C:/Kai.png" -> ".png"
    path_save = "./"  # ./ là thư mục đang chạy này
    name = "encode_Img" # Tên (Không cần đuôi)
    cv2.imwrite(path_save + name + tail, cip) #  Lưu file
    pathnew=path_save + name + tail
    return pathnew

def connect():
    print("Nhap key: ")
    key=str(input())
    print("Connecting...")
    while True:
        try: 
            client, addr = s.accept()
            client.send(bytes(key,"utf8"))
            functions(client,addr,key)
            break
        except:
            print("Run Client.py, Please")
    
def functions(client,addr,key):
    print("Chon cach truyen tin:")
    print("1: Chat")
    print("2: Send file text")
    print("3: Send image")
    print("4: End")
    x=int(input())
    if x==1:
        chat(client,addr,key)
    elif x==2:
        sendtext(client,addr,key)
    elif x==3:
        sendImage(client,addr,key)
    else:
        print("END")
        return

def chat(client,addr,key):
    print("Chat:")
    try:
        print('Connected by', addr)
        while True:
            data = client.recv(1024)
            strdata = data.decode("utf8")
            str_data=decryptedText(strdata,key)
            if str_data == "quit":
                functions(client,addr)
            print("Client: " + str_data)

            msg = str(input("Server: "))
            ci_msg=cipherText(msg,key)
            client.send(bytes(ci_msg,"utf8"))
    finally:
        client.close()

def sendtext(client,addr,key):
    print("Send file text:")
    try:
        print('Connected by', addr)
        print("Nhap duong dan file text muon gui: ") #"D:/vscode/code Python/truyen_nhan_tin/VDK.txt"
        path=str(input())
        with open(path,'rb') as f:
            #l=cipherText(f.read(),key)
            #client.send(l)
            client.send(f.read())
            f.close()
        
        data = client.recv(1024)
        str_data = data.decode("utf8")
        if str_data == "ok":
            functions(client,addr)
    except:
        connect()        

def sendImage(client,addr,key):
    print("send image")
    print("Nhap duong dan gui anh: ")
    path=str(input())
    #D:/vscode/code Python/truyen_nhan_tin/Doremon.jpg
    pathnew=deImage_k(path,key)
    try:
        #print('Connected by', addr)
        with open(pathnew,'rb') as f:
            #im=Image.open()
            #im.show()
            client.send(f.read())
            f.close

        data = client.recv(1024)
        str_data = data.decode("utf8")
        if str_data == "ok":
            functions(client,addr)
            deletepath(pathnew)
    except:
        connect()


 
    
if __name__ == "__main__":
    connect()
#key:VuxDDinhkhaideptraisieucapvippro%%%%%%%%%%%%$$$$$$$$$###########
# git remote add origin https://github.com/VuDinhKhai/socket_server_client.git
# git branch -M main
# git push -u origin main
# https://github.com/VuDinhKhai/socket_server_client.git