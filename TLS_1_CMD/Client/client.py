import socket
import ssl

HOST = 'server'
PORT = 8000

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Ignore certificate verification for testing

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)

secure_socket.connect((HOST, PORT))
print("[*] Connected to server using TLS 1.0")

secure_socket.send(b"Hello, TLS 1.0 Server!")

response = secure_socket.recv(1024).decode()
print("[Server]: " + str(response))

secure_socket.close()
