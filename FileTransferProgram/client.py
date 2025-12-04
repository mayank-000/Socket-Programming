import socket
import os

host = socket.gethostbyname(socket.gethostname())
port = 6060

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    file_path = input("Enter the path of the file to send: ")

    if not os.path.isfile(file_path):
        print("File does not exist. Please check the path and try again.")
        client_socket.close()
        exit()

    filename = os.path.basename(file_path)

    file_size = os.path.getsize(file_path)
    print(f"Preparing to send file: {filename} ({file_size} bytes)")

    response = client_socket.recv(1024).decode('utf-8')

    if response == "Ready to receive filename":
        with open(file_path, 'rb') as f:
            bytes_sent = 0
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break

                client_socket.send(chunk)
                bytes_sent += len(chunk)

                progress = (bytes_sent / file_size) * 100
                if bytes_sent % (4096 * 10) == 0:
                    print(f"Sent {bytes_sent} bytes ({progress:.2f}%)", end='', flush=True)

        print(f"\nFile {filename} sent successfully.")

        final_msg = client_socket.recv(1024).decode('utf-8')
        print(f"Server response: {final_msg}")
except ConnectionRefusedError:
    print("Could not connect to the server. Please ensure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client_socket.close()