from io import BytesIO
from transaction import Tx
import requests

def get_tx(tx_id):
    url = 'https://mempool.space/api/tx/' + tx_id + '/hex'
    r = requests.get(url)
    return r.text

if __name__=='__main__':
    tx_input = input('Add input: ')
    tx_serialized = get_tx(tx_input)
    #tx_serialized = get_tx('f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16')
    tx_serialized = BytesIO(bytes.fromhex(tx_serialized))
    tx = Tx.parse(tx_serialized)
    print(tx)
    print("Now let's show the inputs")
    print(tx.getInputs())
    for txh_in in tx.getInputs():
        tx_in = Tx.parse(BytesIO(bytes.fromhex(get_tx((txh_in.prev_tx_id).hex()))))
        print(tx_in)

