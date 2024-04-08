import socket
import threading

# 服务器IP和端口
HOST = '127.0.0.1'
PORT = 12345

# 创建服务器的socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# 客户端列表和昵称列表
clients = []
nicknames = []

def broadcast(message, _sender=None):
    for client in clients:
        if client != _sender:
            client.send(message)

def handle_client(client):
    while True:
        try:
            # 广播消息
            message = client.recv(1024)
            broadcast(message, client)
        except:
            # 移除和关闭客户端
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # 接受连接
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # 请求并存储昵称
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)


        print(f'Nickname of the client is {nickname}!')
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))


        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
