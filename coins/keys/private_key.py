import secrets

from utils.coding import base58_check_decode, base58_check_encode

from .base import BaseKey
from .public_key import BitcoinPublicKey, PublicKey


class PrivateKey(BaseKey):
    public_key_class = PublicKey

    def get_public_key(self):
        return self.public_key_class.from_private_key(self._value, self._version_byte)

    def get_address(self):
        return self.get_public_key().get_address()

    def to_compressed_wif(self):
        return base58_check_encode(
            self._value + b'\x01',
            version_byte=128 + self._version_byte
        )

    @classmethod
    def from_compressed_wif(cls, compressed_wif: str):
        value, version = base58_check_decode(compressed_wif)
        return cls(
            value[:-1],
            version_byte=version - 128
        )

    @classmethod
    def generate(cls, maximum_value: int=2**256, length: int=32):
        return cls(secrets.randbelow(maximum_value).to_bytes(length, byteorder='big'), version_byte=0)


class BitcoinPrivateKey(PrivateKey):
    N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    public_key_class = BitcoinPublicKey

    @classmethod
    def generate(cls, maximum_value: int=N, length: int=32, network: str='mainnet'):
        version_byte = {
            'mainnet': 0,
            'testnet': 111,
        }[network]
        return cls(secrets.randbelow(maximum_value).to_bytes(length, byteorder='big'), version_byte=version_byte)
