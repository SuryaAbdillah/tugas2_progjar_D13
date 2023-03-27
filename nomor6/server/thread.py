import socket
import select
import queue
from threading import Thread
from time import sleep
from random import randint
import sys
import os

class ProcessThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.q = queue.Queue()
        self.queClient = queue.Queue()

    def add(self, data, client_socket):
        self.q.put(data)
        self.queClient.put(client_socket)

    def stop(self):
        self.running = False
    
    def run(self):
        q = self.q
        queClient = self.queClient
        while self.running:
            try:
                # value itu nilai dari data
                value = q.get(block=True, timeout=1)
                client_socket = queClient.get(block=True, timeout=1)
                process(value, client_socket)
            except queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()

        if not q.Empty():
            print("Element left in queue:")
            while not q.empty():
                print(q.get())

t = ProcessThread()
t.start()

# proses dari masing-mmasing thread di sini
def process(request, client_socket):
    dir = os.path.dirname(os.path.realpath(__file__))

    data = request.decode('utf-8')
    request_header = data.split('\r\n')

    if request_header[0] == '':
        client_socket.close()

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

        client_socket.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
    
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
            client_socket.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

        elif os.path.exists(file_path):
            if file_path.endswith('.html'):
                with open(file_path, 'r') as f:
                    response_data = f.read()
                content_len = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                            + str(content_len) + '\r\n\r\n'
                client_socket.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
            
            else:
                with open(file_path, 'rb') as f:
                    response_data = f.read()
                content_len = len(response_data)
                response_header = 'HTTP/1.1 200 OK\r\nContent-Dispotition: attachment; filename="' + \
                        os.path.basename(file_path) + \
                        '"\r\nContent-Type: application/octet-stream\r\nContent-Length:' \
                            + str(content_len) + '\r\n\r\n'
                client_socket.sendall(response_header.encode('utf-8') + response_data)

        else:
            f = open(os.path.join(dir, '404.html'), 'r')
            response_data = f.read()
            f.close()

            content_len = len(response_data)
            response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                        + str(content_len) + '\r\n\r\n'
            client_socket.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

    sleep(randint(1,5))

# fungsi mengambil KONFIGURASI
# file_name = "httpserver.conf"
# conf = {}
# def get_configuration():
#     flag = False
#     with open(file_name) as configuration:
#         for line in configuration:
#             if line == "# INTEGER":
#                 flag = True
#             else:
#                 if flag == True:
#                     line = line.rstrip("\n")
#                     key = line.split()[0]
#                     value = int(line.split()[-1])
#                     conf[key] = value
#                 else:
#                     line = line.rstrip("\n")
#                     key = line.split()[0]
#                     value = line.split()[-1]
#                     conf[key] = value
    # print(conf)

def get_configuration():
    global conf
    conf = {
    "HOST": "localhost",
    "PORT": 5005,
    "BUFFER_SIZE": 4096,
    "LISTEN_NUM": 5
    }

def main():
    get_configuration()
    print("HALO")
    server_address = (conf.get('HOST'), conf.get('PORT'))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    print(f"Listening on port {conf.get('PORT')}")
    server_socket.listen(conf.get('LISTEN_NUM'))
    input_socket = [server_socket]
    try:
        while True:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            
            for sock in read_ready:
                if sock == server_socket:
                    client_socket, client_address = server_socket.accept()
                    input_socket.append(client_socket)
                else:
                    data = client_socket.recv(conf.get('BUFFER_SIZE'))
                    t.add(data, client_socket)


                # client_socket, client_address = server_socket.accept()
                # ready = select.select([client_socket, ], [], [], 2)
                # if ready[0]:
                #     data = client_socket.recv(conf.get('BUFFER_SIZE'))
                #     t.add(data, client_socket)
                # else:
    except KeyboardInterrupt:
        print("Stop.")
        sys.exit(0)
    cleanup()

def cleanup():
    t.stop()
    t.join()

if __name__=="__main__":
    main()
