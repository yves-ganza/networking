#!/usr/bin/env python3
from socket import *

HOST = '127.0.0.1'
PORT = 3000


def sendFile(connection, filename):
    try:
        f = open(filename)
        resp = f.readlines()
        for i in range(len(resp)):
            connection.send(resp[i].encode('utf-8'))
            connection.send('\r\n'.encode('utf-8'))
        f.close()
        connection.close()
    except error as e:
        return e


with socket(AF_INET, SOCK_STREAM) as serversocket:
    serversocket.bind((HOST, PORT))
    serversocket.listen()
    print(f'Listening on port {PORT}...')
    conn, addr = serversocket.accept()
    print(f'New connection from {addr}')
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            req = message.split()[1]
            print(f'{req} requested')
            if(req == '/'):
                header = 'HTTP/1.1 200 OK\n'
                header += 'Content-Type: text/html\n\n'
                header = header.encode('utf-8')
                conn.send(header)
                sendFile(conn, 'index.html')
                break
            else:
                raise IOError
        except error as e:
            header = 'HTTP/1.1 404 Not Found\n'
            conn.send(header.encode('utf-8'))
            sendFile(conn, 'err.html')
            print(e)
            break
