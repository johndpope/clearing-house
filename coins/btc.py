import hashlib
from typing import List, Union

import ecdsa

import settings
from builders.coins.btc import BlockchainInfo
from coins.keys import BitcoinAddress, BitcoinPrivateKey, BitcoinPublicKey
from utils.types import varint, varstr


class BTC:
    def __init__(self, network: str='mainnet'):
        self._network = network
        self.blockchain_provider = BlockchainInfo(network=network)

    def create_private_key(self):
        return BitcoinPrivateKey.generate(network=self._network)

    def get_unspent_transactions(self, addresses: Union[List[str], str]):
        if isinstance(addresses, str):
            return self.blockchain_provider.unspent(addresses)
        result = []
        for address in addresses:
            result.append(self.blockchain_provider.unspent(address))
        return result

    def get_balance(self, address: str) -> int:
        return self.blockchain_provider.balance(address)

    def serialize_transaction(self, transaction, script_signature=None):
        result = bytearray()
        result.extend(transaction['version'].to_bytes(4, byteorder='little'))
        result.extend(varint(len(transaction['inputs'])))

        for input_transaction in transaction['inputs']:
            result.extend(
                bytes.fromhex(
                    input_transaction['outpoint']['hash']
                )
            )
            result.extend(
                input_transaction['outpoint']['index'].to_bytes(4, byteorder='little')
            )
            input_script = bytes.fromhex(script_signature or input_transaction['script'])
            if input_script:
                result.extend(varint(len(input_script)))
                result.extend(input_script)
            result.extend(b'\xff\xff\xff\xff')
        result.extend(varint(len(transaction['outputs'])))
        for output_transaction in transaction['outputs']:
            result.extend(
                output_transaction['value'].to_bytes(8, byteorder='little')
            )
            output_script = bytes.fromhex(output_transaction['script'])
            result.extend(varint(len(output_script)))
            result.extend(output_script)

        result.extend(b'\x00\x00\x00\x00')
        return result.hex()

    def sign_transaction(self, transaction, private_key: BitcoinPrivateKey):
        serialized_transaction = bytes.fromhex(self.serialize_transaction(transaction) + '01000000')
        s256 = hashlib.sha256(
            hashlib.sha256(serialized_transaction).digest()
        ).digest()

        sk = ecdsa.SigningKey.from_string(private_key.to_bytes(), curve=ecdsa.SECP256k1)
        sig = sk.sign_digest(s256, sigencode=ecdsa.util.sigencode_der) + b'\01'
        public_key = private_key.get_public_key().to_bytes()
        script_signature = varstr(sig).hex() + varstr(public_key).hex()
        signed_transaction = self.serialize_transaction(transaction, script_signature=script_signature)
        return signed_transaction

    def push(self, signed_transaction):
        self.blockchain_provider.push(signed_transaction)

    def create_transaction(
        self, inputs: list, outputs: list,
        change_address: str, fee: int=0,
    ):
        transaction = {
            'locktime': 0, 'version': 1, 'inputs': [], 'outputs': []
        }
        total_input_sum = 0
        total_output_sum = 0
        for input_transaction in inputs:
            total_input_sum += input_transaction['value']
            transaction['inputs'] += [{
                'outpoint': {
                    'hash': input_transaction['output'],
                    'index': input_transaction['output_n'],
                },
                'script': input_transaction['script'],
            }]
        for output in outputs:
            total_output_sum += output['value']
            transaction['outputs'] += [{
                'script': BitcoinAddress.from_wif(output['address']).to_script(),
                'value': output['value'],
            }]

        if total_input_sum < total_output_sum + fee:
            raise Exception('Not enough money')

        # What is the fuck '5430'?
        elif total_input_sum > total_output_sum + fee + 5430:
            transaction['outputs'] += [{
                'script': BitcoinAddress.from_wif(change_address).to_script(),
                'value': total_input_sum - total_output_sum - fee,
            }]
        return transaction


btc = BTC(settings.BITCOIN_NETWORK)


def get_btc():
    return btc
