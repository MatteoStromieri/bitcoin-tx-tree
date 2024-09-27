import json
from helpers import varint2int, get_tx
from io import BytesIO
import hashlib

class Tx():

    def __init__(self, id, version, inputs, outputs, locktime):
        self.id = id
        self.version = version    # 4 byte, int
        self.inputs = inputs      # var len, bytes
        self.outputs = outputs    # var len, bytes
        self.locktime = locktime  # 4 byte, int
    
    @classmethod
    def parse(cls, r, id):
        version = int.from_bytes(r.read(4), 'little')
        numin = varint2int(r)
        inputs = [TxIn.parse(r) for _ in range(numin)]
        numout = varint2int(r)
        outputs = [TxOut.parse(r) for _ in range(numout)]
        locktime = int.from_bytes(r.read(4), 'little')
        return cls(id, version, inputs, outputs, locktime)

    def getInputs(self):
        return self.inputs

    def __str__(self):
        inputs = [txin.__str__() for txin in self.inputs]
        outputs = [txout.__str__() for txout in self.outputs]
        out = {'version': self.version, 'inputs':inputs,\
               'outputs': outputs, 'locktime': self.locktime}
        return json.dumps(out)

    def isCoinbase(self):
        if (len(self.inputs) == 1 and self.inputs[0].prev_tx_id == bytes(32) and self.inputs[0].vout == 0xffffffff):
            return True
        return False

class SegWitTx(Tx):

    def __init__(self, id, version, marker, flag, inputs, outputs, locktime):
        super().__init__(id, version, inputs, outputs, locktime)
        self.marker = marker      # 1 byte
        self.flag = flag          # 1 byte
        # da implementare il parsing del witness

    @classmethod
    def parse(cls, r, id):
        version = int.from_bytes(r.read(4), 'little')
        marker = r.read(1)
        flag = r.read(1)
        numin = varint2int(r)
        inputs = [TxIn.parse(r) for _ in range(numin)]
        numout = varint2int(r)
        outputs = [TxOut.parse(r) for _ in range(numout)]
        locktime = int.from_bytes(r.read(4), 'little')
        # aggiungere parsing del Witness
        return cls(id, version, marker, flag, inputs, outputs, locktime)
    
    # in input ho uno stream di byte di una transazione
    @classmethod    
    def isSegWit(cls, r):
        r.seek(4)
        marker = r.read(1)
        flag = r.read(1)
        r.seek(0)

        if marker == b'\x00' and flag == b'\x01':
            return True
        return False

class TxIn:

    def __init__(self, prev_tx_id, vout, script, sequence = 0xffffffff):
        self.prev_tx_id = prev_tx_id         # 32 byte
        self.vout = vout                # 4 byte
        self.script = script           # var len, byes
        self.sequence = sequence       # 4 byte, int

    @classmethod
    def parse(cls, r):
        prev_tx_id = r.read(32)[::-1]
        vout = int.from_bytes(r.read(4), 'little')
        script_len = varint2int(r)
        script = r.read(script_len)
        sequence = int.from_bytes(r.read(4), 'little')
        return cls(prev_tx_id, vout, script, sequence)
    
    def __str__(self):
        out = {'prev_tx_id':self.prev_tx_id.hex(), 'vout': self.vout, \
               'script': self.script.hex(), 'sequence': self.sequence}
        return json.dumps(out)


class TxOut:

    def __init__(self, amount, script):
        self.amount = amount   # 8 byte, int
        self.script = script   # var len, bytes

    @classmethod
    def parse(cls, r):
        amount = int.from_bytes(r.read(8), 'little')
        script_len = varint2int(r)
        script = r.read(script_len)
        return cls(amount, script)

    def __str__(self):
        out = {'amount': self.amount, 'script': self.script.hex()}
        return json.dumps(out)


if __name__ == '__main__':
    tx_id = input("Your tx: ")
    serialized_tx = get_tx(tx_id)
    if (SegWitTx.isSegWit(serialized_tx)):
            tx = SegWitTx.parse(serialized_tx)
    else:
        tx = Tx.parse(serialized_tx)
    print(tx.isCoinbase())
