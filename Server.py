#!/usr/bin/env python

import socket

'''
Server listens for request containing two numbers
and then sums those numbers. The server responds with
the summation
'''

class Server:

    def __init__(self, host=socket.gethostbyname("localhost"), port=54003):
        self.socket = socket.socket()
        self.socket.bind((host, port))

    def close(self):
        self.socket.close()

    def _add(self, a, b):
        return str(int(a) + int(b))

    def listen(self):
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        while True:
            data = conn.recv(1024).decode()
            numbers = data.split(" ")
            sum = self._add(numbers[0], numbers[1])
            conn.send(sum.encode())

if __name__ == "__main__":
    server = Server()
    server.listen()