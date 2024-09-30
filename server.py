import socket

class TcpServer:
    def __init__(self):
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host: str = ''
        self.server_port: int = 9001
        
        self.FILE_PATH: str = './tgt/received_video.mp4'

        self.header: int = 32
        self.buffer: int = 1460
        # サーバのストレージ（バイト単位）
        self.storage_size: int = 4398046511104
        self.MAX_FILE_SIZE: int = 2**32

        self.RECEIVE_FILE_SIZE_EXCEED: int = 1
        

    # ソケットバインド
    def _bind(self):
        self.sock.bind((self.server_host, self.server_port))
        self.sock.listen(1)
        print('Waiting for connection...')
    
    # 通信
    def communication(self):
        self._bind()
        conn, addr = self.sock.accept()
        print(f'Connected from {addr}')
        
        # ファイルバイト数取得
        file_size = conn.recv(self.header)
        file_size = int.from_bytes(file_size, byteorder='big')

        # ファイルバイト数が4GBを超えている場合
        if file_size > self.MAX_FILE_SIZE:
            conn.sendall(self.RECEIVE_FILE_SIZE_EXCEED.to_bytes(self.header, byteorder='big'))
            return 1
        
        # ビデオファイル受信
        with open(self.FILE_PATH, 'wb') as f:
            while file_size > 0:
                data = conn.recv(self.buffer)
                file_size -= self.buffer
                f.write(data)
        
        # レスポンスの送信
        conn.sendall('Video file uploaded'.encode())


def main():
    server: TcpServer = TcpServer()
    server.communication()
    server.sock.close()

main()