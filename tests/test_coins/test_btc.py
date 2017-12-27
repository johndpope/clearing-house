from __future__ import absolute_import

import unittest
from test.requests_mock import RequestsMock

from coins import BTC
from coins.keys import PrivateKey
from tests.test_coins.test_data import (TEST_ADDRESS, TEST_ADDRESS_2,
                                        TEST_PRIVATE_KEY,
                                        TEST_UNSPENT_TRANSACTIONS)


class TestBtcTestnet(unittest.TestCase):
    def setUp(self):
        self.btc = BTC('testnet')
        self.requests_mock = RequestsMock()
        self.requests_mock.start()

    def tearDown(self):
        self.requests_mock.stop()

    def create_transaction(self):
        self.requests_mock.set_response_value(TEST_UNSPENT_TRANSACTIONS)
        transactions = self.btc.get_unspent_transactions(TEST_ADDRESS)
        my_transaction = self.btc.create_transaction(
            inputs=transactions,
            outputs=[{'address': TEST_ADDRESS_2, 'value': 50_000_000}],
            change_address=TEST_ADDRESS,
        )
        return my_transaction

    def test_serialize_transaction(self):
        my_transaction = self.create_transaction()
        self.assertEqual(self.btc.serialize_transaction(my_transaction), '01000000010e3a560bf81142a78a475352d2e0479e5b3842539dcaa6e64a2c2f7d1cb3d7e7000000001976a914dd2dfec702815f6348bff8600965c97da473f31488acffffffff0280f0fa02000000001976a914b9d58015bd232601e8179a6335f255a1ee89e8ed88ac408fe108000000001976a914aafc95cbfb2b6e6ebb9cb21beafb23bed5c3d1c888ac00000000')

    def test_sign_transaction(self):
        my_transaction = self.create_transaction()
        self.btc.sign_transaction(my_transaction, PrivateKey.from_compressed_wif(TEST_PRIVATE_KEY))
