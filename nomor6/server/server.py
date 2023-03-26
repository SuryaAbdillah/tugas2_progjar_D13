import socket
import select
import sys
import os


with open('httpserver.conf', 'r') as f:
    PORT = int(f.readlines()[1])

f.close()

dir = os.path.dirname(os.path.realpath(__file__))

server_address = ('localhost', PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]


try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)                       
            
            else:                
                # receive data from client, break when null received          
                data = sock.recv(4096).decode('utf-8')

                request_header = data.split('\r\n')
                if request_header[0] == '':
                    sock.close()
                    input_socket.remove(sock)
                    continue

                request_file = request_header[0].split()[1]
                response_header = b''
                response_data = b''

                if request_file == 'index.html' or request_file == '/' or request_file == '/index.html':
                    f = open('index.html', 'r')
                    response_data = f.read()
                    f.close()
                    
                    content_len = len(response_data)
                    response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'

                    sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                else:
                    file_path = dir + request_file
                    if os.path.isdir(file_path):
                        contents = os.listdir(file_path)
                        response_data = '<html><body><ul>'

                        for item in contents:
                            response_data += f'<li><a href="{request_file}/{item}">{item}</a></li>'
                        response_data += '</ul></body></html>'

                        content_len = len(response_data)
                        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'
                        sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                    elif os.path.exists(file_path):
                        if file_path.endswith('.html'):
                            with open(file_path, 'r') as f:
                                response_data = f.read()
                            content_len = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'
                            sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
                        
                        else:
                            with open(file_path, 'rb') as f:
                                response_data = f.read()
                            content_len = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Dispotition: attachment; filename="' + \
                                    os.path.basename(file_path) + \
                                    '"\r\nContent-Type: application/octet-stream\r\nContent-Length:' \
                                      + str(content_len) + '\r\n\r\n'
                            sock.sendall(response_header.encode('utf-8') + response_data)

                    else:
                        f = open(os.path.join(dir, '404.html'), 'r')
                        response_data = f.read()
                        f.close()

                        content_len = len(response_data)
                        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                    + str(content_len) + '\r\n\r\n'
                        sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))


except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)

