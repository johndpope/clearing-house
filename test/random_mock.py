import secrets
from unittest import mock


class RandomMock:
    def __init__(self):
        self.mock = mock.patch.object(
            secrets,
            'randbelow',
            mock.Mock(side_effect=range(1, 10000000)),
        )

    def __enter__(self):
        self.mock.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock.stop()
