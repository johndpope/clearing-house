from utils.coding import base58_check_decode, base58_check_encode

from .base import BaseKey


class Address(BaseKey):
    @classmethod
    def from_wif(cls, value: str):
        decoded_value, version = base58_check_decode(value)
        return cls(decoded_value, version_byte=version)

    def to_wif(self):
        return base58_check_encode(
            self._value,
            version_byte=self._version_byte
        )


class BitcoinAddress(Address):
    def to_script(self):
        wif_form = self.to_wif()
        if wif_form[0] == '3' or wif_form[0] == '2':
            return 'a914' + self.to_hex() + '87'
        else:
            return '76a914' + self.to_hex() + '88ac'
