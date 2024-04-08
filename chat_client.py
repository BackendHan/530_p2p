import socket
import threading

# 选择昵称
nickname = input("Choose your nickname: ")

# 连接到服务器
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))

def receive():
    while True:
        try:
            # 接收来自服务器的消息
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # 发生错误时关闭连接
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

# 开始接收和写入的线程
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
