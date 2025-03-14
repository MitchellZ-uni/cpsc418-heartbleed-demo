import socket
import ssl

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 8000

# Create SSL context forcing TLS 1.0
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("[*] Server listening on " + str(HOST) + ":" + str(PORT) + " using TLS 1.0...")

tls_socket = context.wrap_socket(server_socket, server_side=True)

while True:
    client_socket, addr = tls_socket.accept()
    print("[+] Connection from " + str(addr))

    data = client_socket.recv(1024).decode()
    print("[Client]: " + str(data))

    response = "Hello, secure client!"
    client_socket.send(response.encode())

    client_socket.close()
