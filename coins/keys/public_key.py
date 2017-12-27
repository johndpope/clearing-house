import hashlib

import ecdsa

from .address import Address, BitcoinAddress
from .base import BaseKey


class PublicKey(BaseKey):
    address_class = Address

    def get_address(self):
        x = hashlib.new('ripemd160', hashlib.sha256(self._value).digest()).digest()
        return self.address_class.from_bytes(x, self._version_byte)

    @staticmethod
    def _compress_key(key: bytes):
        x, y = key[:32], key[32:]
        suffix = 2 + (y[-1] % 2)
        return bytes([suffix]) + x

    @staticmethod
    def from_private_key(private_key, version_byte):
        sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
        return PublicKey(PublicKey._compress_key(sk.verifying_key.to_string()), version_byte)


class BitcoinPublicKey(PublicKey):
    address_class = BitcoinAddress
