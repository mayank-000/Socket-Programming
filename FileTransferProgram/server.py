import socket
import os

host = socket.gethostbyname(socket.gethostname())
port = 6060

SAVE_FOLDER = "received_files"

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)
    print(f"Created directory: {SAVE_FOLDER}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Server listening on {host}:{port}")

while True:
    try:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established!")

        file_name = client_socket.recv(1024).decode('utf-8')

        client_socket.send("Ready to receive filename".encode('utf-8'))

        filepath = os.path.join(SAVE_FOLDER, file_name)

        with open(filepath, 'wb') as f:
            bytes_received = 0
            while True:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break

                f.write(chunk)
                bytes_received += len(chunk)

                if bytes_received % (4096 * 10) == 0:
                    print(f"Received {bytes_received} bytes...", end='', flush=True)

        print(f"\nFile {file_name} received successfully and saved to {filepath}")

        client_socket.send("File received successfully".encode('utf-8'))

        client_socket.close()

    except KeyboardInterrupt:
        print("\nServer is shutting down.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

server_socket.close()
