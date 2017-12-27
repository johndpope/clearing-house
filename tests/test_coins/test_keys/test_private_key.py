import unittest

from coins.keys import PrivateKey
from tests.test_coins.test_data import (TEST_ADDRESS, TEST_MAINNET_ADDRESS,
                                        TEST_MAINNET_PRIVATE_KEY,
                                        TEST_MAINNET_PRIVATE_KEY_INT,
                                        TEST_PRIVATE_KEY, TEST_PRIVATE_KEY_INT,
                                        TEST_PUBLIC_KEY)


class TestPrivateKey(unittest.TestCase):
    def setUp(self):
        pass

    def test_from_wif(self):
        private_key = PrivateKey.from_compressed_wif(TEST_PRIVATE_KEY)
        self.assertEqual(private_key.to_int(), TEST_PRIVATE_KEY_INT)

    def test_from_wif_mainnet(self):
        private_key = PrivateKey.from_compressed_wif(TEST_MAINNET_PRIVATE_KEY)
        self.assertEqual(private_key.to_int(), TEST_MAINNET_PRIVATE_KEY_INT)

    def test_public_key(self):
        private_key = PrivateKey.from_compressed_wif(TEST_PRIVATE_KEY)
        self.assertEqual(private_key.get_public_key().to_hex(), TEST_PUBLIC_KEY)

    def test_address(self):
        private_key = PrivateKey.from_compressed_wif(TEST_PRIVATE_KEY)
        self.assertEqual(private_key.get_address().to_wif(), TEST_ADDRESS)

    def test_address_mainnet(self):
        private_key = PrivateKey.from_compressed_wif(TEST_MAINNET_PRIVATE_KEY)
        self.assertEqual(private_key.get_address().to_wif(), TEST_MAINNET_ADDRESS)
