import socket
from html.parser import HTMLParser

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('its.ac.id', 80)
client_socket.connect(server_address)

request_header = b'GET / HTTP/1.0\r\nHost: 103.94.189.5\r\n\r\n'
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
status = response.split("\r\n")[0].split(maxsplit=1)[1]
status_code = status.split(maxsplit=1)[0]
deskripsi = status.split(maxsplit=1)[1]

print("========= NOMOR 1 =========")
print(f"STATUS\t: {status}")
print(f"STATUS CODE\t: {status_code}")
print(f"DESKRIPSI CODE\t: {deskripsi}")

# NOMOR 2
# Cetaklah versi Content-Encoding dari HTTP response header di halaman web its.ac.id
hasil = response.split("\r\n")
content = filter(lambda a: 'Content-Type' in a, hasil)
content = list(content)[0].split()[1]
print("\n========= NOMOR 2 =========")
print(f"CONTENT TYPE: {content}")

# NOMOR 3
# Cetaklah versi HTTP dari HTTP response header pada halaman web its.ac.id
http = response.split("\r\n")[0].split(maxsplit=1)[0]
print("\n========= NOMOR 3 =========")
print(f"VERSI HTTP: {http}")

# coba HTML PARSER
# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print("Encountered a start tag:", tag)

#     def handle_endtag(self, tag):
#         print("Encountered an end tag :", tag)

#     def handle_data(self, data):
#         print("Encountered some data  :", data)

# parser = MyHTMLParser()
# parser.feed(response)
