import socket

import mmp

class TcpServer:
    def __init__(self):
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host: str = ''
        self.server_port: int = 9001
        
        self.FILE_PATH: str = './tgt/received_video.mp4'

        self.header: int = 8
        self.buffer: int = 1460
        # サーバのストレージ（バイト単位）
        self.storage_size: int = 4398046511104
        self.MAX_FILE_SIZE: int = 2**40

        self.RECEIVE_FILE_SIZE_EXCEED: int = 1


    # ソケットバインド
    def _bind(self):
        self.sock.bind((self.server_host, self.server_port))
        self.sock.listen(1)
        print('Waiting for connection...')

    # データ受信
    def recv(self):
        self._bind()
        conn, addr = self.sock.accept()
        print(f'Connected from {addr}')
        
        header: bytes = conn.recv(self.header)
        file_size: int = mmp.get_payload_size(header)

        # ファイルバイト数が4TBを超えている場合
        if file_size > self.MAX_FILE_SIZE:
            conn.sendall(self.RECEIVE_FILE_SIZE_EXCEED.to_bytes(self.header, byteorder='big'))
            conn.close()
            return 1
        
        data: bytes = b''
        # ビデオファイル受信
        while file_size > 0:
            data += conn.recv(self.buffer)
            file_size -= self.buffer
        
        return data

    # 通信
    def communication(self):
        
        # レスポンスの送信
        conn.sendall('Video file uploaded'.encode())
    


class VideoFileServer:
    def __init__(self, data: bytes):
        self.TMP_FILE_PATH: str = './tmp/received_video.mp4'
        self.recv_data: bytes = data
    
    # 一時領域に保存
    def save_tmp(self):
        with open(self.TMP_FILE_PATH, 'wb') as f:
            f.write(self.recv_data)


    # 動画圧縮
    def video_compression(self):
        pass

    # 解像度の変更
    def chenge_video_resolution(self):
        pass

    # アスペクト比の変更
    def change_video_aspect_ratio(self):
        pass

    # 音声へ変換
    def convert_video_to_audio(self):
        pass

    # GIF、WEBMを作成
    def create_gif_webm(self):
        pass
    



def main():
    server: TcpServer = TcpServer()
    server.communication()
    server.sock.close()

main()