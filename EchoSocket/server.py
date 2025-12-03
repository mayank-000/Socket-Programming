import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

host = socket.gethostbyname(socket.gethostname())
port = 6060

server_socket.bind((host, port))
print(f"Socket binded to port {host}:{port}")

server_socket.listen(1)
print("Socket is listening")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address} has been established!")

while True:
    message = client_socket.recv(1024).decode('utf-8') # .decode() = Bytes -> String
    if message.lower() == 'exit':
        print("Closing connection")
        break

    client_socket.send(message.encode('utf-8'))
    print(f"Echoed message: {message}")

client_socket.close()
server_socket.close()
