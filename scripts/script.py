from evm_indexer.fetcher import Fetcher
from home.models import NativeTx, ERC20Tx
from evm_indexer.internal_tracer import InternalTracer
from web3 import Web3
import csv

from web3.exceptions import BadFunctionCallOutput

ERC20_TRANSFER_EVENT_SIGNATURE_HASH = Web3.keccak(text="Transfer(address,address,uint256)").hex()


class Decoder:
    def __init__(self, fetcher):
        self.fetcher = fetcher
        self.web3 = fetcher.web3

    def get_erc20_transfers_from_tx(self, tx_receipt):
        # Filter the logs for ERC20 Transfer events
        transfer_events = []
        for log in tx_receipt['logs']:
            if log['topics'][0] == ERC20_TRANSFER_EVENT_SIGNATURE_HASH and len(log['topics']) == 3:
                try:
                    from_address = self.web3.to_checksum_address('0x' + log['topics'][1][-40:])
                    to_address = self.web3.to_checksum_address('0x' + log['topics'][2][-40:])
                    token_address = log['address']
                    amount = Web3.to_int(hexstr=log['data'])

                    transfer_events.append({
                        'hash': tx_receipt['transactionHash'],
                        'from': from_address,
                        'to': to_address,
                        'amount': amount,
                        'token_address': token_address
                    })
                except BadFunctionCallOutput:
                    # Handle error if the log decoding fails
                    continue
        return transfer_events

    def get_native_transfers_from_tx(self, tx_hash):
        tx = self.web3.eth.get_transaction(tx_hash)
        from_address = self.web3.to_checksum_address(tx['from'])
        to_address = self.web3.to_checksum_address(tx['to'])
        gas = tx['gas']
        gasPrice = tx['gasPrice']
        blockHash = self.web3.to_hex(tx['blockHash'])
        blockNumber = self.web3.to_hex(tx['blockNumber'])
        gasPrice = tx['gasPrice']
        hash = self.web3.to_hex(tx['hash'])
        input = self.web3.to_hex(tx['input'])
        nonce = tx['nonce']
        transactionIndex = tx['transactionIndex']
        v = tx['v']
        r = self.web3.to_hex(tx['r'])
        s = self.web3.to_hex(tx['s'])
        value = tx['value']

        return [{
            'hash': hash,
            'blockNumber': blockNumber,
            'from': from_address,
            'to': to_address,
            'amount': value,
            'token_address': None,
            'blockHash': blockHash,
            'gasPrice': gasPrice,
            'input': input,
            'gas': gas,
            'nonce': nonce,
            'transactionIndex': transactionIndex,
            'v': v,
            'r': r,
            's': s,
        }]


def run():
    # Set the node URL
    # NODE_URL = 'https://seed.omchain.io'
    # NODE_URL = 'http://35.185.112.219:4545/' #testnet
    NODE_URL = 'http://34.73.228.200:4545'  # mainet

    # Initialize fetcher, decoder, and internal tracer
    fetcher = Fetcher(NODE_URL, is_poa=True)
    decoder = Decoder(fetcher=fetcher)
    internal_tracer = InternalTracer(NODE_URL)

    nativeTxGenerated = None
    ERC20Tx.objects.all().delete()
    NativeTx.objects.all().delete()

    for i in range(29904448, 29904550):


        # Fetch transactions from a specific block
        fetched_transactions = fetcher.fetch_transactions_in_block(i)

        # Process each transaction
        tx_receipts = [internal_tracer.get_tx_receipt(tx['hash'])['result'] for tx in fetched_transactions]
        tx_data = {tx_receipt['transactionHash']: [internal_tracer.get_trace(tx_receipt['transactionHash']), tx_receipt]
                   for
                   tx_receipt in tx_receipts if tx_receipt['status'] == '0x1'}
        # Extract different types of transactions
        native_transactions = [decoder.get_native_transfers_from_tx(tx_data[tx][1]['transactionHash']) for tx in
                               tx_data]

        if(len(native_transactions) == 0):
            print("Empty block!")
        else:
            print("Block: ", i)

        for nattxs in native_transactions:
            for nt in nattxs:
                nativeTxGenerated = NativeTx.objects.create(
                    hash=nt['hash'],
                    blockNumber=int(nt['blockNumber'], 16),
                    fromAddr=nt['from'],
                    toAddr=nt['to'],
                    tokenAddress=nt['token_address'],
                    blockHash=nt['blockHash'],
                    gasPrice=nt['gasPrice'],
                    inputTx=nt['input'],
                    gas=nt['gas'],
                    nonce=nt['nonce'],
                    transactionIndex=nt['transactionIndex'],
                    v=nt['v'],
                    r=nt['r'],
                    s=nt['s']
                )

                print("Adding native hash:  " + nt['hash'])
                print(" ")

        erc20_transactions = [decoder.get_erc20_transfers_from_tx(tx_data[tx][1]) for tx in tx_data]

        for erc20txs in erc20_transactions:
            for e20tx in erc20txs:
                ERC20Tx.objects.create(
                    hash=e20tx['hash'],
                    fromAddr=e20tx['from'],
                    toAddr=e20tx['to'],
                    amount=e20tx['amount'],
                    tokenAddress=e20tx['token_address'],
                    nativeTx=nativeTxGenerated
                )

                print("Adding erc20 to nativeTransaction:  " + e20tx['hash'])