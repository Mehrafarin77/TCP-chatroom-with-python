import threading
import socket

nickname = input('Choose a nickname: ').capitalize()

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'Nickname: ':
                client.send(nickname.encode('utf-8'))
            else:
                print(msg)
        except:
            print('Error!')
            client.close()
            break


def send_msg():
    while True:
        msg = f'{nickname}: {input("")}'
        if msg.split()[1].strip() == 'quit':
            client.send(f'{nickname} has left the chat room!'.encode('utf-8'))
            client.close()
            break
        client.send(msg.encode('utf-8'))


recv_thread = threading.Thread(target=receive)
recv_thread.start()

send_thread = threading.Thread(target=send_msg)
send_thread.start()

