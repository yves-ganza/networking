from socket import *
import sys

if(len(sys.argv) < 3):
    print('Usage: python3 client.py IPaddress Port')
    sys.exit(2)

try:
    HOST = gethostbyname(sys.argv[1])
except error as e:
    print("Host name could'nt be resolved")
    sys.exit(2)

PORT = sys.argv[2]

with socket(AF_INET, SOCK_STREAM) as s:
    s.connect((HOST, int(PORT)))
    request = 'GET /www.python.org HTTP/1.1\r\n\r\n'
    try:
        s.sendall(request.encode('utf-8'))
    except error as e:
        print('Request send failed')
        sys.exit(2)
    received = []
    while 1:
        data = s.recv(1024)
        if(len(data) < 1):
            print('No data received')
            break
        print(data.decode('utf-8'))
    sys.exit(0)
