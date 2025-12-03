import socket
import threading

nickname = input("Enter your nickname: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 6060

client_socket.connect((host, port))
print(f"Connected to the server at {host}:{port}")

def receive():
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICK':
                client_socket.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            client_socket.close()
            break

def write():
    
    while True:
        try:
            message = f"{nickname}: {input('')}"
            client_socket.send(message.encode('utf-8'))
        except:
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()