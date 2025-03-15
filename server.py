import http.server
# import socket
import ssl

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 8000

# Create a HTTPS server
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        client_ip, client_port = self.client_address
        print("[*] Connection from " + str(client_ip) + ":" + str(client_port))

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TLS 1.0 HTTPS Example</title>
        </head>

        <body>
            <h1>Welcome to the TLS 1.0 HTTPS Example</h1>
            <p>This page is served over a secure HTTPS connection using TLS 1.0 protocol.</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

httpd = http.server.HTTPServer((HOST, PORT), CustomHTTPRequestHandler)

# Load OpenSSL with heartbeat enabled
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Configure the server to use TLS 1.0
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print("[*] Server listening on " + str(HOST) + ":" + str(PORT) + " using TLS 1.0...")

# Start the server
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Shutting down the server...")
    httpd.server_close()
