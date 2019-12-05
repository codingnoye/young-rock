import socket
import threading

CLIENT = ('127.0.0.1', 3001)
SERVER = ('127.0.0.1', 3002)

class Socket:
    _sock = None
    _pair = None
    def listen(self, callback):
        while True:
            data = _pair.recv(1024)
            if not data:
                break
            callback(data)
    
    def send(self, data):
        

class Server:
    _sock = None
    def __init__(self):
        if Server._sock == None:
            Server._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Server._sock.bind(SERVER)
    
    # Thread
    def wait(self):
        Server._sock.listen()
        Server._pair = _sock.accept()
        print(f'Connected by {Server._pair}')
        
    @property
    def sock(self):
        return Server.__sock

if __name__ == "__main__":
    Server().send('hello')
