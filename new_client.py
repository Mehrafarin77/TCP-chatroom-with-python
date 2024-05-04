import socket
import threading

nickname = input('Choose a nickname: ').capitalize()

# Constant
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

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


def send():
    while True:
        msg = f'{nickname}: {input("")}'
        if msg.split()[1].strip() == 'quit':
            client.close()
            break
        client.send(msg.encode('utf-8'))


recv_thread = threading.Thread(target=receive)
recv_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()