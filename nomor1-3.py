import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('its.ac.id', 80)
client_socket.connect(server_address)

request_header = b'GET / HTTP/1.0\r\nHost: www.python.org\r\n\r\n'
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')

print(response)
client_socket.close()

# NOMOR 1
# Cetaklah status code dan deskripsinya dari HTTP response header pada halaman its.ac.id

# NOMOR 2
# Cetaklah versi Content-Encoding dari HTTP response header di halaman web its.ac.id

# NOMOR 3
# Cetaklah versi HTTP dari HTTP response header pada halaman web its.ac.id