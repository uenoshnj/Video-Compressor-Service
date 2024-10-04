import json

# 受信用
def _get_header(data: bytes) -> bytes:
    return data[:8]

def _get_body(data: bytes) -> bytes:
    return data[8:]

def get_json_size(data: bytes) -> int:
    header: bytes = _get_header(data)
    return int.from_bytes(header[:2], 'big')

def get_mediatype_size(data: bytes) -> int:
    header: bytes = _get_header(data)
    return int.from_bytes(header[2:3], 'big')

def get_payload_size(data: bytes) -> int:
    header: bytes = _get_header(data)
    return int.from_bytes(header[3:8], 'big')

def get_json(data: bytes) -> dict:
    body: bytes = _get_body(data)
    json_size: int = get_json_size(data)
    return json.loads(body[:json_size].decode())

def get_mediatype(data: bytes) -> bytes:
    body: bytes = _get_body(data)
    json_size: int = get_json_size(data)
    mediatype_size: int = get_mediatype_size(data)
    return body[json_size:json_size+mediatype_size].decode()

def get_payload(data: bytes) -> bytes:
    body: bytes = _get_body(data)
    json_size: int = get_json_size(data)
    mediatype_size: int = get_mediatype_size(data)
    return body[json_size+mediatype_size:]

# 送信用
def create_packet(json_data: json, mediatype: str, payload: bytes) -> bytes:
    json_size = len(json_data.encode('utf-8')).to_bytes(2, 'big')
    mediatype_size = len(mediatype.encode('utf-8')).to_bytes(1, 'big')
    payload_size = len(payload).to_bytes(5, 'big')

    return json_size + mediatype_size + payload_size + json_data.encode('utf-8') + mediatype.encode('utf-8') + payload