import secrets

from utils.coding import base58_check_decode, base58_check_encode


class BaseKey:
    def __init__(self, value: bytes, version_byte: int=0):
        self._value = value
        self._version_byte = version_byte

    @classmethod
    def from_bytes(cls, value: bytes, version_byte: int = 0):
        return cls(value, version_byte=version_byte)

    @classmethod
    def from_hex(cls, value: str, version_byte: int = 0):
        return cls(bytes.fromhex(value), version_byte=version_byte)

    @classmethod
    def from_int(cls, value: int, version_byte: int = 0, length: int = 0):
        return cls(value.to_bytes(length, byteorder='big'), version_byte=version_byte)

    @classmethod
    def from_wif(cls, value: str):
        decoded_value, version = base58_check_decode(value)
        return cls(decoded_value, version_byte=version - 128)

    def to_bytes(self):
        return self._value

    def to_int(self):
        return int.from_bytes(self._value, byteorder='big')

    def to_hex(self) -> str:
        return self._value.hex()

    def to_wif(self):
        return base58_check_encode(
            self._value,
            version_byte=128 + self._version_byte
        )
