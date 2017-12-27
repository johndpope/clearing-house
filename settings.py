import logging
import os
from logging.config import dictConfig

from flask import request

from utils import env

ENVIRONMENT = env.type

BITCOIN_NETWORK = 'testnet'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False

if ENVIRONMENT == 'production':
    DEBUG = 0
    LOCALHOST = '0.0.0.0'
    PORT = int(os.environ['PORT'])
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']
elif ENVIRONMENT in {'development', 'testing'}:
    DEBUG = 1
    LOCALHOST = 'localhost'
    PORT = 8080
    from secure_settings import SECRET_KEY
    from secure_settings import SQLALCHEMY_DATABASE_URI
    from secure_settings import WTF_CSRF_SECRET_KEY


def configure_logging():
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.path = request.full_path
            record.method = request.method
            record.remote_addr = request.remote_addr
            record.request_id = request.request_id
            return super().format(record)

    dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '%(message)s',
            },
            'request_formatter': {
                '()': RequestFormatter,
                'format': (
                    '%(remote_addr)s - - [%(asctime)s] %(request_id)s "%(method)s %(path)s" %(message)s'
                )
            }
        },
        'handlers': {
            'default': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
            'request_handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'request_formatter',
            },
        },
        'loggers': {
            'werkzeug': {
                'level': 'INFO',
                'handlers': [],
                'propagate': False,
            },
            'request_logger': {
                'level': 'INFO',
                # ToDO: Fix this shit when logging to file will be enabled
                'handlers': ['request_handler'] if ENVIRONMENT != 'testing' else [],
                'propagate': False,
            },
        },
        'root': {
            'level': 'ERROR',
            'handlers': ['default'],
        }
    })
