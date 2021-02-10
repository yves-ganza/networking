from socket import *

import sys

if(len(sys.argv) <= 1):
    print(
        'Usage: "python3 proxyserver.py server_ip"\n[server_ip is the IP address of the proxy server]')
    sys.exit(2)

def sendErr(clientsocket):
    clientsocket.send(b'HTTP/1.1 404 Not Found\r\n')
    with open('err.html', 'r') as errfile:
        data = errfile.readlines()
        for i in range(len(data)):
            clientsocket.send(data[i].encode('utf-8'))
        clientsocket.send(b'\r\n')

# Create a server socket, bind it to a port and start listening
HOST = str(sys.argv[1])
PORT = 5354

tcpSerSoc = socket(AF_INET, SOCK_STREAM)
tcpSerSoc.bind((HOST, PORT))

tcpSerSoc.listen()
print(f'Listening on port {PORT}')

while 1:
    # Start receiving data from the client
    print('Ready to serve...')

    tcpCliSoc, addr = tcpSerSoc.accept()
    print(f'New connection from {addr}')

    message = tcpCliSoc.recv(1024).decode('utf-8')
    print(message)

    headers = message.split('\r\n')
    header_dic = {}
    for header in headers[1:]:
        header_dic[header.split(':')[0]] = header.split(':')[1:]

    # Extract the file from the given message
    filename = message.split()[1].partition('/')[2]
    print(f'Requested file: {filename}')

    fileExists = False

    filetouse = '/'+filename
    print(f'File to use {filetouse}')

    try:
        # check wether the file exists in the cache
        f = open(filename, 'rb')
        responsedata = f.readlines()
        fileExists = True

        # Proxyserver finds hit in cache and generates a response
        for i in range(len(responsedata)):
            tcpCliSoc.send(responsedata[i])
        f.close()
        print('Read from cache\n')
    # Error handling for file not found in cache
    except IOError:
        if(not fileExists):
            # Create a socket on the proxy server
            with socket(AF_INET, SOCK_STREAM) as c:
                hostn = filename.replace('www.', '', 1)
                print(f'Host name: {hostn}')
                try:
                    # Ask port 80 for the file requested by the client
                    c.connect((hostn, 80))
                    request = f'GET / HTTP/1.1\r\n\r\n'
                    c.sendall(request.encode('utf-8'))
                    responsedata = []
                    statusRead = False

                    # Read response into buffer
                    while True:
                        data = c.recv(1024)
                        if(len(data) < 1):
                            break
                        if(not statusRead):
                            statusLine = data.decode('utf-8').split('\r\n')[0].split()
                            status = int(statusLine[1])
                            statusRead = True
                            print(f'Status {status}')
                        # Create a new file in the cache for the requested file
                        # Also send the response in the buffer to the client and the corresponding file to the cache
                        tcpCliSoc.send(data)
                        responsedata.append(data)
                    #Check status of the response and save data to cache
                    if(len(responsedata) > 0 and status < 400):
                        with open('./'+filename, 'wb') as tmpfile:
                            tmpfile.writelines(responsedata)
                            print('[Wrote to cache]\n')

                except error as e:
                    print(e)
                    print('Illegal request')
        else:
            sendErr(tcpCliSoc)
    # close the client socket and server socket
    tcpCliSoc.close()
tcpSerSoc.close()
sys.exit()
