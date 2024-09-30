import socket
import sys
import os

class TcpClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host: str = ''
        self.server_port: int = 9001

        self.buffer: int = 1460
    
    def _connect(self) -> None:
        try:
            self.sock.connect((self.server_host, self.server_port))
        except:
            print('fail to connect Server')
            self.sock.close()
            sys.exit(1)
    


    def communication(self, filepath: str, file_size: int) -> None:
        
        self._connect()

        self.sock.send(file_size.to_bytes(32, 'big'))

        with open(filepath, 'rb') as f:
            data = f.read(self.buffer)
            while file_size > 0:
                file_size -= self.sock.send(data)
                data = f.read(self.buffer)
        
        print('video file sent')

        data = self.sock.recv(self.buffer)
        print(data.decode())


class Mp4FileClient:
    def __init__(self):
        self.file_path: str = ''
        self.file_size: int
    
    def input_file_path(self) -> None:
        # ファイルパスの入力
        self.file_path = input('input file path: ')
        self._file_validate(self.file_path)


    # ファイルの検証
    def _file_validate(self, filepath: str) -> None:
        # ファイルの存在確認
        if not os.access(filepath, os.F_OK) :
            print('file is not exist')
            sys.exit(1)

        # ファイルの読み込み権限確認
        if not os.access(filepath, os.R_OK) :
            print('Permission denied')
            sys.exit(1)
        
        # ファイルの拡張子確認
        if not filepath.endswith('.mp4') :
            print('Invalid file extension')
            sys.exit(1)
        
        #　ファイルサイズの確認
        self.file_size = os.path.getsize(filepath)
        if self.file_size > 2**32 :
            print('File size is too large')
            sys.exit(1)
        


def main():
    file = Mp4FileClient()
    file.input_file_path()

    client = TcpClient()
    client.communication(file.file_path, file.file_size)
    client.sock.close()

main()