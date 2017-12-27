import json

import requests


class BaseBuilder:
    def __init__(self):
        self._session = requests.Session()

    def request(self, method, url, response_processor=None, *args, **kwargs):
        response_processor = response_processor or self.process_response
        return response_processor(
            self._session.request(method, url, *args, **kwargs)
        )

    def get(self, url, *args, **kwargs):
        return self.request('get', url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.request('post', url, *args, **kwargs)

    @staticmethod
    def process_response(response):
        return json.loads(response.text)
