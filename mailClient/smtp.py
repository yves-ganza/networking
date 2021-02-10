from socket import *
import ssl
import base64
import time
import sys

if len(sys.argv) < 5:
    print('Error: Not Enough Arguments\nUsage: python3 smtp.py FROMemail TOemail password mailserver')
    sys.exit(2)

username = sys.argv[1]
password = sys.argv[3]
server = sys.argv[4]
receiver = sys.argv[2]

msg = '\r\n I love networking'
endmsg = '\r\n.\r\n'

# Mail server to send to
mailserver = server

# Create socket and establish a TCP connection with mail server
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((mailserver, 25))
recv = clientsocket.recv(1024).decode()

if recv[:3] != '220':
   print('220 reply not recieved from server')
   clientsocket.close()

# Send HELO command to server
heloCommand = 'HELO World\r\n'
clientsocket.send(heloCommand.encode())
recv1 = clientsocket.recv(1024).decode()

if recv1[:3] != '250':
    print('250 reply not received from server')
    clientsocket.close()

# Send STARTTLS command
clientsocket.send('STARTTLS\r\n'.encode())
recv_tls = clientsocket.recv(1024).decode()
print('Receipt after STARTTLS command: ', recv_tls)

# Start ssl connection
ssl_socket = ssl.wrap_socket(clientsocket, ssl_version=ssl.PROTOCOL_SSLv23)

# Send AUTH LOGIN command
ssl_socket.send('AUTH LOGIN\r\n'.encode())
recv_auth = ssl_socket.recv(1024).decode()
print('Receipt after AUTH LOGIN command: ', recv_auth)

# Authenticate
ssl_socket.send(base64.b64encode(username.encode())+ "\r\n".encode())
ssl_socket.send(base64.b64encode(password.encode())+ "\r\n".encode())
recv_auth = ssl_socket.recv(1024).decode()
print('Receipt after authentication command: ', recv_auth)

# Send MAIL FROM command
mailfrom = f'MAIL FROM:<{username}>\r\n'
ssl_socket.send(mailfrom.encode())
recv3 = ssl_socket.recv(1024).decode()
print('Receipt after MAIL FROM command: ', recv3)

# Send RCPT TO command
rcptto = f'RCPT TO:<{receiver}>\r\n'
ssl_socket.send(rcptto.encode())
recv4 = ssl_socket.recv(1024).decode()
print('Receipt after RCPT TO command: ', recv4)

# Send Data command
data = 'DATA\r\n'.encode()
ssl_socket.send(data)
recv5 = ssl_socket.recv(1024).decode()
print('Receipt after DATA command: ', recv5)

# Send message data
subject = 'Suject: Hello World\r\n\r\n'
date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())+'\r\n\r\n'
ssl_socket.send(subject.encode())
ssl_socket.send(date.encode())
ssl_socket.send(msg.encode())

# Message ends with a single period
ssl_socket.send(endmsg.encode())
recv_msg = ssl_socket.recv(1024).decode()
print('Receipt after sending email: ', recv_msg)

# Send QUIT command
ssl_socket.send('QUIT\r\n'.encode())
recv_quit = ssl_socket.recv(1024).decode()
print('Receipt after QUIT command: ', recv_quit)

ssl_socket.close()

