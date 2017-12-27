import unittest

from utils.types import (process_netaddr, process_varint, process_varstr,
                         varint, varstr)


class TestUtils(unittest.TestCase):
    def test_varint(self):
        self.assertEqual(varint(0x42), b'\x42')
        self.assertEqual(varint(0x123), b'\xfd\x23\x01')
        self.assertEqual(varint(0x12345678), b'\xfe\x78\x56\x34\x12')
        self.assertEqual(process_varint(varint(0x42)), [0x42, 1])
        self.assertEqual(process_varint(varint(0x1234)), [0x1234, 3])

    def test_varstr(self):
        self.assertEqual(varstr(b'abc'), b'\x03abc')
        self.assertEqual(process_varstr(b'\x03abc'), [b'abc', 4])

    def test_processAddr(self):
        self.assertEqual(process_netaddr(b'x' * 20 + b'\x62\x91\x98\x16\x20\x8d'), '98.145.152.22:8333')
