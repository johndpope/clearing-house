from unittest import mock


class RequestsMock:
    def __init__(self):
        self.response_value = None
        self.patch = mock.patch(
            'builders.base.BaseBuilder.request',
            side_effect=lambda *args, **kwargs: self.response_value
        )

    def start(self):
        self.patch.start()

    def stop(self):
        self.patch.stop()

    def set_response_value(self, value):
        self.response_value = value
