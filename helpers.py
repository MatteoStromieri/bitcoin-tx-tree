import requests
from io import BytesIO

def get_tx(tx_id):
    url = 'https://mempool.space/api/tx/' + tx_id + '/hex'
    r = requests.get(url)
    #print(r.text)
    return BytesIO(bytes.fromhex(r.text))


def varint2int(r):
    first_byte = int.from_bytes(r.read(1), 'little')
    if first_byte < 253:
        return first_byte
    if first_byte == 253:
        return int.from_bytes(r.read(2), 'little')
    if first_byte == 254:
        return int.from_bytes(r.read(4), 'little')
    if first_byte == 255:
        return int.from_bytes(r.read(8), 'little')

def getVarIntBytes(r):
    index = r.tell()
    bytes = r.read(1)
    first_byte = int.from_bytes(bytes, 'little')
    if first_byte < 253:
        r.seek(index)
        return bytes
    if first_byte == 253:
        bytes = bytes + r.read(2)
        r.seek(index)
        return bytes
    if first_byte == 254:
        bytes = bytes + r.read(4)
        r.seek(index)
        return bytes
    if first_byte == 255:
        bytes = bytes + r.read(8)
        r.seek(index)
        return bytes
