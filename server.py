import socket

class TcpServer:
    def __init__(self):
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host: str = ''
        self.server_port: int = 9001
        self.client_host: str = ''
        self.client_port: int = 0

        self.buffer: int = 1460
        # サーバのストレージ（バイト単位）
        self.storage_size: int = 4398046511104
        

    # ソケットバインド
    def _bind(self):
        self.sock.bind((self.server_host, self.server_port))
        self.sock.listen(1)
    

    
