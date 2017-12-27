from ..base import BaseBuilder


class BlockchainInfo(BaseBuilder):
    def __init__(self, network: str='mainnet'):
        super(BlockchainInfo, self).__init__()
        self._network = network
        self._base_url = 'https://{}blockchain.info'.format(
            '' if self._network == 'mainnet' else self._network + '.'
        )

    def unspent(self, address):
        data = self.get(
            self._base_url + '/unspent',
            params={'active': address},
        )
        result = []
        for output in data["unspent_outputs"]:
            result.append({
                'output': output['tx_hash'],
                'output_n': output['tx_output_n'],
                'value': output['value'],
                'confirmations': output['confirmations'],
                'script': output['script']
            })
        return result

    def balance(self, address):
        data = self.get(
            self._base_url +
            '/q/addressbalance/{}/'.format(address),
            response_processor=lambda x: int(x.content),
            params={'confirmations': 6},
        )
        return data

    def push(self, signed_transaction):
        return self.post(
            self._base_url + '/pushtx',
            data={'tx': signed_transaction}
        )
