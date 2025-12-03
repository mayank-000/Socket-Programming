import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

host = socket.gethostbyname(socket.gethostname())
port = 6060

client_socket.connect((host, port))
print(f"Connected to server at {host}:{port}")
while True:
    message = input("Enter message to send (type 'exit' to quit) {client}: ")
    client_socket.send(message.encode('utf-8')) # .encode() = String -> Bytes

    if message.lower() == 'exit':
        print("Closing connection")
        break

    response = client_socket.recv(1024).decode('utf-8')

client_socket.close()
