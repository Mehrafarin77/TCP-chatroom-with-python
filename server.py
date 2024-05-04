import threading
import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6000

clients = []
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print('server is listening...')

def broadcast(msg):
    for client in clients:
        # the server sends the msg to all clients
        client.send(msg.encode('utf-8'))


def handle_client(client):
    while True:
        try:
            # server receives a message from the client
            message = client.recv(1024).decode('utf-8')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            print(f'{nickname} has left the chat room!')
            broadcast(f'{nickname} has left the chat room!')
            nicknames.remove(nickname)
            client.close()
            break


def main():
    while True:
        # connection with a client
        client, addr = server.accept()
        print(f'Connection is established with {addr}')

        # send a message to the connected client for his name
        client.send('Nickname: '.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'{nickname} got connected.')
        broadcast(f'{nickname} joined the chat room!')

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()