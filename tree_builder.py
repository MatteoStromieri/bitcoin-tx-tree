from transaction import Tx, SegWitTx
from helpers import get_tx
from io import BytesIO

class TreeBuilder:

    @classmethod
    def buildTree(cls, root_tx, height = float('inf')):
        #print(root_tx)
        root = Node(root_tx)
        # we can omit the following piece of code since coinbase txs have
        # no input
        if root_tx.isCoinbase():
            return root
        if height > 0:
            for txh_in in root_tx.getInputs():
                hex_tx = (txh_in.prev_tx_id).hex()
                _tx_in = get_tx(hex_tx)
                if (SegWitTx.isSegWit(_tx_in)):
                    tx = SegWitTx.parse(_tx_in, hex_tx)
                else:
                    tx = Tx.parse(_tx_in, hex_tx)
                child = TreeBuilder.buildTree(tx, height - 1)
                root.addChild(child)
        return root

class Node:

    def __init__(self, root):
        self.root = root
        self.children = []

    def addChild(self, node):
        self.children.append(node)

if __name__ == '__main__':
    tx_hex = get_tx('f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16')
    tx_in = Tx.parse(tx_hex)
    TreeBuilder.buildTree(tx_in)
