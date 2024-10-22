import json
import socket

import ffmpeg

import mmp

class TcpServer:
    def __init__(self):
        self.sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host: str = ''
        self.server_port: int = 9001
        
        self.json_obj: dict = {}
        self.tmp_file: str = './tmp/tmp_file'
        self.media_type: str = ''
        self.output: str = './output/output'

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
        
        # ヘッダー受信
        header: bytes = conn.recv(self.header)
        file_size: int = mmp.get_payload_size(header)
        json_size: int = mmp.get_json_size(header)
        media_type_size: int = mmp.get_mediatype_size(header)

        # ファイルバイト数が4TBを超えている場合
        if file_size > self.MAX_FILE_SIZE:
            error_obj = ErrorHandle(self.RECEIVE_FILE_SIZE_EXCEED, 'File size exceeds 4TB', 'Reduce file size')
            conn.sendall(mmp.create_packet(error_obj, '', b''))
            conn.close()
            return 1
        
        # jsonの受信
        self.json_obj = json.load(conn.recv(json_size).decode('utf-8'))

        # 一時保存ファイル名を作成
        self.media_type: str = conn.recv(media_type_size).decode('utf-8')
        self.tmp_file += self.media_type

        # ビデオファイル受信
        with open(self.tmp_file, 'wb') as f:
            while file_size > 0:
                data: bytes = conn.recv(self.buffer)
                file_size -= self.buffer
                f.write(data)

    # 通信
    def communication(self):
        
        # レスポンスの送信
        conn.sendall('Video file uploaded'.encode())


class ErrorHandle:
    def __init__(self, error_code: int, message: str, solusion: str):
        self.error_obj: dict = {
            'code' : error_code,
            'message' : message,
            'solusion': solusion
        }
    
    


class VideoProcessor:
    def __init__(self, tmp_file: str, output: str, media_type: str, json_obj: dict):
        self.tmp_file: str = tmp_file
        self.output: str = output
        self.media_type: str = media_type
        self.json_obj: dict = json_obj
        self.functions: dict[str, function] = {
            '1': self.compress,
            '2': self.chenge_resolution,
            '3': self.change_aspect_ratio,
            '4': self.convert_to_audio,
            '5': self.create_gif_webm
        }   


    # 動画圧縮
    def compress(self):
        self.output = self.output + self.media_type
        ffmpeg -i self.tmp_file -crf 28 self.output

    # 解像度の変更
    def chenge_resolution(self, width: int, height: int):
        self.output = self.output + self.media_type
        ffmpeg -i self.tmp_file -vf scale={width}:{height} self.output
        

    # アスペクト比の変更
    def change_aspect_ratio(self, width: int, height: int):
        self.output = self.output + self.media_type
        ffmpeg -i self.tmp_file -aspect {width}:{height} self.output

    # 音声へ変換
    def convert_to_audio(self):
        self.output = self.output + '.aac'
        ffmpeg -i self.tmp_file -vn -c:a aac self.output

    # GIF、WEBMを作成
    def create_gif_webm(self):
        pass
    
    # 処理判断
    def process_Handle(self):
        self.json_obj
        



def main():
    server: TcpServer = TcpServer()
    server.communication()
    server.sock.close()

main()