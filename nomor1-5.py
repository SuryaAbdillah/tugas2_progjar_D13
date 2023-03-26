# REFERENSI: https://gist.github.com/ndavison/6a5d97cb8a9091cffa7a

# IMPORT LIBRARY
import socket
import ssl
from bs4 import BeautifulSoup as soup

class HTTPS:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT

        self.connect()
        self.SSL()
        self.request()
        self.receive()
        self.save_response()
        self.get_status()
        self.get_encoding()
        self.get_httpver()
        self.get_charset()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

    def SSL(self):
        context = ssl.create_default_context()
        self.sock = context.wrap_socket(self.sock, server_hostname=self.HOST)

    def request(self):
        self.sock.send(f"GET / HTTP/1.1\r\nHost:{self.HOST}\r\n\r\n".encode())

    def receive(self):
        self.response = ''
        while True:
            data = self.sock.recv(4096)
            self.response += data.decode('utf-8')
            if not data:
                self.sock.close()
                break
        self.response_len = len(self.response)
        self.header = self.response.split('<!DOCTYPE html>', maxsplit=1)[0]
        self.content = self.response.split('<!DOCTYPE html>', maxsplit=1)[1]
    
    def save_response(self):
        f = open(f"{self.HOST}_response.txt", "w+")
        f.write(self.response)
        f.close()

    def get_status(self):
        self.status = self.header.split("\r\n", 1)[0].split(maxsplit=1)[1]
        self.status_code = self.status.split()[0]
        self.status_desc = self.status.split()[1]
        print("\n========= STATUS CODE =========")
        print(self.status)
        print(f"STATUS CODE\t: {self.status_code}")
        print(f"STATUS DESKRIPSI: {self.status_desc}")

    def get_encoding(self):
        partition_header = self.header.split("\r\n")
        # Transfer-Encoding
        if any("Transfer-Encoding" in word for word in partition_header):
            self.transfer = list(filter(lambda a: 'Transfer-Encoding' in a, partition_header))[0]
            self.transfer =self.transfer.split()[1]
            print("\n========= TRANSFER ENCODING =========")
            print(f"TRANSFER ENCODING: {self.transfer}")
        else:
            print("\nMAAF TRANSFER-ENCODING TIDAK DITEMUKAN DALAM HEADER")

        # Accept-Encoding
        if any("Accept-Encoding" in word for word in partition_header):
            self.accept = list(filter(lambda a: 'Accept-Encoding' in a, partition_header))[0]
            self.accept = self.accept.split()[0][:-1]
            print("\n========= ACCEPT ENCODING =========")
            print(f"ACCEPT ENCODING: {self.accept}")
        else:
            print("\nMAAF Accept-Encoding TIDAK DITEMUKAN DALAM HEADER")
    
    def get_httpver(self):
        self.httpver = self.header.split("\r\n", 1)[0].split(maxsplit=1)[0]
        print("\n========= HTTP VERSION =========")
        print(f"VERSION: {self.httpver}")

    def get_charset(self):
        partition_header = self.header.split("\r\n")
        if any("charset" in word for word in partition_header):
            self.charset = list(filter(lambda a: 'charset' in a, partition_header))[0].split()[2]
            self.charset =self.charset.split("=",1)[1]
            print("\n========= CHARSET =========")
            print(f"charset: {self.charset}")
        else:
            print("\nMAAF charset TIDAK DITEMUKAN DALAM HEADER")

def parsing(response):
    doc = soup(response, "html.parser")
    direktori = []
    masuk_ul = doc.find("ul", {"class": "navbar-nav h-100 wdm-custom-menus links"})
    try:
        list_li = masuk_ul.find_all('li')
        for menu in list_li:
            panduan = menu.find('a')
            if panduan:
                direktori.append(panduan.text.strip())
            masuk_div = menu.find('div')
            dropdown = masuk_div.find_all('a')
            for dropDown in dropdown:
                direktori.append('\t' + dropDown.text.strip())
    except AttributeError:
        pass

    print("\n========= HASIL DIREKTORI =========")
    for list_direktori in direktori:
        print(list_direktori)

# NOMOR 1 - 3
print("\n\n========= ITS.AC.ID =========")
https = HTTPS("www.its.ac.id", 443)

# NOMOR 4 - 5
print("\n\n========= CLASSROOM.ITS.AC.ID =========")
https_2 = HTTPS("classroom.its.ac.id", 443)
parsing(https_2.response)
