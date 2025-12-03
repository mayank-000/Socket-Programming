import socket
import threading

clients = []
nicknames = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 6060

server_socket.bind((host, port))
server_socket.listen()
print(f"Server started on {host}:{port}")

def brodcast(message): # defining 'brodcast' function to send message to all clients
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            brodcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            brodcast(f"{nickname} left the chat!".encode('utf-8'))
            nicknames.remove(nickname)
            print(f"{nickname} disconnected")
            break

def receive():
    while True:
        client, address = server_socket.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        brodcast(f"{nickname} joined the chat!".encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()