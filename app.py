import logging
import traceback
import uuid
from exceptions import BaseError

from flask import Flask, jsonify, request

import settings
from db import get_db
from routes import configure_routes
from utils.json import ExploitableJSONEncoder

app = Flask(__name__)
app.config.from_object(settings)
app.json_encoder = ExploitableJSONEncoder

get_db().init_app(app)

configure_routes(app)
settings.configure_logging()


request_logger = logging.getLogger('request_logger')


@app.before_request
def persist_request_id():
    request.request_id = request.headers.get('X-Request-ID', str(uuid.uuid1()))


@app.after_request
def log_request(response):
    request_logger.info(
        '{status_code} {content_length}'.format(
            status_code=response.status_code,
            content_length=response.calculate_content_length() or '-',
        )
    )
    return response


@app.errorhandler(Exception)
def handle_exception(exception):
    request_logger.error('\n' + traceback.format_exc())
    if isinstance(exception, BaseError):
        response = jsonify(exception.as_dict())
        response.status_code = exception.status_code
    else:
        response = jsonify({'status': 'error', 'message': str(exception)})
        response.status_code = 500
    return response
