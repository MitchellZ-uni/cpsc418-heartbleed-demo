import http.server
import ssl
import uuid
from urllib.parse import parse_qs

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 8000
SESSIONS = {}  # Session store map, id->{type->data}

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def get_session(self):
        # Check for existing session cookie
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookies = cookie_header.split(';')
            for cookie in cookies:
                if 'session_id' in cookie:
                    session_id = cookie.split('=')[1].strip()
                    if session_id in SESSIONS:
                        return session_id
        
        # Create new session if none exists
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = {'messages': []}
        return session_id
    
    def do_GET(self):
        client_ip, client_port = self.client_address
        print("[*] Connection from " + str(client_ip) + ":" + str(client_port))

        session_id = self.get_session()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Set-Cookie", "session_id={0}; Path=/".format(session_id))
        self.end_headers()

        # Get session messages
        session_messages = SESSIONS[session_id]['messages']

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TLS 1.0 HTTPS Server</title>
        </head>

        <body>
            <h1>TLS 1.0 HTTPS Server</h1>
            <form action="/" method="post">
                <input type="text" name="message" placeholder="Enter a message">
                <button type="submit">Send</button>
            </form>
            <h2>Your Session Messages:</h2>
            <ul>
                {0}
            </ul>
        </body>
        </html>
        """.format(
            "".join("<li>{0}</li>".format(msg) for msg in session_messages)
        )
        self.wfile.write(html.encode())
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))  # Get request body size
        post_data = self.rfile.read(content_length).decode()  # Read and decode the data

        # Parse the POST data
        data = parse_qs(post_data)
        message = data.get('message', [''])[0]

        session_id = self.get_session()
        
        client_ip, client_port = self.client_address
        print("[*] Received data from ", client_ip, ":", client_port)
        print("Data saved in Session {0}: {1}".format(session_id, message))
        
        # Store message in session
        SESSIONS[session_id]['messages'].append(message)

        # Send response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Set-Cookie", "session_id={0}; Path=/".format(session_id))
        self.end_headers()
        
        response_message = """
        <h1>Data Received!</h1>
        <p>Message: {0}</p>
        <p><a href="/">Go Back</a></p>
        """.format(message)
        self.wfile.write(response_message.encode())

def main():
    # Create a HTTPS server
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

if __name__ == "__main__":
    main()