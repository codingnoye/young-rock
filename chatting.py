import socket
import threading

SERVER = ('127.0.0.1', 3003)

class Socket:
    def recv(self, callback):
        def thread(self, callback):
            while True:
                data = self._sock.recv(1024)
                if not data:
                    break
                callback(data.decode())
        threading.Thread(target=thread, args=(self, callback), daemon=True).start()
    
    def send(self, data):
        self._sock.sendall(data.encode())

    @property
    def sock(self):
        return self._sock

class Server(Socket):
    def __init__(self):
        self._sv_sock = None
        self._sock = None
        self._addr = None
        self._sv_sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sv_sock.bind(SERVER)
    # Thread
    def connect(self):
        print('Listening...')
        self._sv_sock.listen()
        self._sock, self._addr = self._sv_sock.accept()
        print(f'Connected by {self._addr}')

class Client(Socket):
    def __init__(self):
        self._sock = None
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        print('Connecting...')
        self._sock.connect(SERVER)
        print(f'Connected to {self._sock.raddr}')

if __name__ == "__main__":
    sock = Server()
    sock.connect()
    sock.recv(print)
    i = input()
    while i != "exit":
        sock.send(i)
        i = input()