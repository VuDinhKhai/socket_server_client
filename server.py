import socket
#import threading
import numpy as np

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

def connect():
    print("Nhap key: ")
    key=str(input())
    print("Connecting...")
    while True:
        try: 
            client, addr = s.accept()
            functions(client,addr)
            break
        except:
            print("Run Client.py, Please")
    
def functions(client,addr):
    print("Chon cach truyen tin:")
    print("1: Chat")
    print("2: Send file text")
    print("3: Send image")
    print("4: End")
    x=int(input())
    if x==1:
        chat(client,addr)
    elif x==2:
        sendtext(client,addr)
    elif x==3:
        sendImage(client,addr)
    else:
        print("END")
        return

def chat(client,addr):
    print("Chat:")
    try:
        print('Connected by', addr)
        while True:
            data = client.recv(1024)
            str_data = data.decode("utf8")
            if str_data == "quit":
                functions(client,addr)
            print("Client: " + str_data)
            msg = str(input("Server: "))
            client.send(bytes(msg,"utf8"))
    finally:
        client.close()

def sendtext(client,addr):
    print("Send file text:")
    try:
        print('Connected by', addr)
        print("Nhap duong dan file text muon gui: ") #"D:/vscode/code Python/truyen_nhan_tin/VDK.txt"
        path=str(input())
        with open(path,'rb') as f:
            client.send(f.read())
            f.close()
        
        data = client.recv(1024)
        str_data = data.decode("utf8")
        if str_data == "ok":
            functions(client,addr)
    except:
        connect()        

def sendImage(client,addr):
    print("send image")
    print("Nhap duong dan gui anh: ")
    path=str(input())
    #D:/vscode/code Python/truyen_nhan_tin/The.jpg
    try:
        #print('Connected by', addr)
        with open(path,'rb') as f:
            #im=Image.open()
            #im.show()
            client.send(f.read())
            f.close

        data = client.recv(1024)
        str_data = data.decode("utf8")
        if str_data == "ok":
            functions(client,addr)
    except:
        connect()


 
    
if __name__ == "__main__":
    connect()

# git remote add origin https://github.com/VuDinhKhai/socket_server_client.git
# git branch -M main
# git push -u origin main
# https://github.com/VuDinhKhai/socket_server_client.git