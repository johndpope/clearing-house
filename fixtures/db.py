import json
import logging
from test import RandomMock, TimeMock

from db import get_db
from settings import configure_logging

from .exceptions import FixtureError

configure_logging()


class DbFixture:
    def __init__(self, app):
        self.app = app
        self.client = app.test_client()

    def __enter__(self):
        self.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()

    def check_reponse(self, r):
        if r.status_code != 200:
            logging.error('Response: %s', r.data)
            raise FixtureError()

    def commit(self):
        get_db().create_all(app=self.app)
        r = self.client.post(
            '/api/v1/tag/',
            data=json.dumps({
                'name': 'science',
                'content': {
                    'translates': {
                        'ru': {
                            'display_name': 'наука',
                        },
                        'en': {
                            'display_name': 'science',
                        }
                    },
                },
            }),
            content_type='application/json'
        )
        self.check_reponse(r)
        r = self.client.post(
            '/api/v1/tag/',
            data=json.dumps({
                'name': 'politics',
                'content': {
                    'translates': {
                        'ru': {
                            'display_name': 'политика',
                        },
                        'en': {
                            'display_name': 'politics',
                        }
                    },
                },
            }),
            content_type='application/json'
        )
        self.check_reponse(r)
        with RandomMock():
            with TimeMock():
                r = self.client.post(
                    '/api/v1/event/',
                    data=json.dumps({
                        'content': {'name': 'test_event_1'},
                        'tags': ['science', 'politics'],
                        'outcomes': [
                            {
                                'content': {'label': 'yes', 'background': '3.jpg'},
                            },
                            {
                                'content': {'label': 'no', 'background': '2.jpg'},
                            },
                        ],
                    }),
                    content_type='application/json'
                )
            self.check_reponse(r)
            with TimeMock(offset=1):
                r = self.client.post(
                    '/api/v1/event/',
                    data=json.dumps({
                        'content': {
                            'translates': {
                                'ru': {
                                    'description': 'Выберут ли Путина президентом?',
                                    'title': 'Выборы Президента России 2018',
                                },
                                'en': {
                                    'description': 'Will Putin be the next President?',
                                    'title': 'President Election 2018 in Russia',
                                }
                            },
                            'name': 'test_event_2',
                            'background': 'goatsy.jpg',
                        },
                        'tags': ['politics',],
                        'outcomes': [
                            {
                                'content': {
                                    'translates': {
                                        'ru': {
                                            'label': 'Да',
                                        },
                                        'en': {
                                            'label': 'Yes',
                                        },
                                    },
                                    'background': 'yes.jpg',
                                },
                            },
                            {
                                'content': {
                                    'translates': {
                                        'ru': {
                                            'label': 'Нет',
                                        },
                                        'en': {
                                            'label': 'No',
                                        },
                                    },
                                    'background': 'no.jpg',
                                },
                            },
                        ],
                    }),
                    content_type='application/json'
                )
            self.check_reponse(r)
            with TimeMock(offset=2):
                r = self.client.post(
                    '/api/v1/event/',
                    data=json.dumps({
                        'content': {
                            'translates': {
                                'ru': {
                                    'description': 'Будет ли импичмент Трампа?',
                                    'title': 'Импичмент Трампа',
                                },
                                'en': {
                                    'description': 'Will Trump be impeached?',
                                    'title': 'Trump Impeachment',
                                }
                            },
                            'name': 'trump_impeachment',
                            'background': 'usa.jpg',
                        },
                        'tags': ['politics', ],
                        'outcomes': [
                            {
                                'content': {
                                    'translates': {
                                        'ru': {
                                            'label': 'Да',
                                        },
                                        'en': {
                                            'label': 'Yes',
                                        },
                                    },
                                    'background': 'yes.jpg',
                                },
                            },
                            {
                                'content': {
                                    'translates': {
                                        'ru': {
                                            'label': 'Нет',
                                        },
                                        'en': {
                                            'label': 'No',
                                        },
                                    },
                                    'background': 'no.jpg',
                                },
                            },
                        ],
                    }),
                    content_type='application/json'
                )
            self.check_reponse(r)

    def rollback(self):
        get_db().drop_all(app=self.app)
