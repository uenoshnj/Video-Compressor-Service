import json

# 受信用
def _get_header(data: bytes):
    return data[:8]

def _get_body(data: bytes):
    return data[8:]

def get_json_size(data: bytes):
    header: bytes = _get_header(data)
    return int.from_bytes(header[:2], 'big')

def get_mediatype_size(data: bytes):
    header: bytes = _get_header(data)
    return int.from_bytes(header[2:3], 'big')

def get_payload_size(data: bytes):
    header: bytes = _get_header(data)
    return int.from_bytes(header[3:8], 'big')


def get_json(data: bytes):
    body: bytes = _get_body(data)
    json_size: int = get_json_size(data)
    return json.loads(body[:json_size].decode())

def get_mediatype(data: bytes):
    body: bytes = _get_body(data)
    json_size: int = get_json_size(data)
    mediatype_size: int = get_mediatype_size(data)
    return body[json_size:json_size+mediatype_size].decode()

def get_payload(data: bytes):
    body: bytes = _get_body(data)
    json_size: int = get_json_size(data)
    mediatype_size: int = get_mediatype_size(data)
    return body[json_size+mediatype_size:]

# 送信用
