import time
from datetime import datetime
from unittest import mock


class TimeMock:
    range = 1000000

    def __init__(self, base_value=int(time.mktime(datetime(2015, 10, 21).timetuple())), offset=0, incrementing=False):
        base_value += offset
        if incrementing:
            base_value = range(base_value, base_value + self.range)
            self.mock = mock.patch.object(
                time,
                'time',
                mock.Mock(side_effect=base_value),
            )
        else:
            self.mock = mock.patch.object(
                time,
                'time',
                mock.Mock(return_value=base_value),
            )

    def __enter__(self):
        self.mock.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mock.stop()
