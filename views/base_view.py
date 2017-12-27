import logging
from exceptions import ValidationError

from flask import jsonify, request
from flask.views import View
from werkzeug.datastructures import CombinedMultiDict

from .base_form import BaseForm

request_logger = logging.getLogger('request_logger')


class BaseView(View):
    _cached_views = {}
    _cached_views_clses = {}
    form = None

    @property
    def logger(self):
        return request_logger

    @classmethod
    def as_view(cls, name, *class_args, **class_kwargs):
        if name not in cls._cached_views:
            cls._cached_views[name] = super(BaseView, cls).as_view(name, *class_args, **class_kwargs)
            cls._cached_views_clses[name] = cls
        if cls != cls._cached_views_clses[name]:
            raise ValueError(
                '`{}` view cannot have the name `{}` as it was assigned previously to {}'.format(
                    cls.__name__, name, cls._cached_views_clses[name].__name__,
                )
            )
        return cls._cached_views[name]

    def __init__(self):
        self.response_values = {}
        self.processed_form = None

    @property
    def lang(self):
        return request.args.get('lang', 'en')

    @property
    def raw_aware_lang(self):
        if self.processed_form and self.processed_form['raw'].data == 1:
            return None
        return self.lang

    def process_request(self, *args, **kwargs):
        raise NotImplementedError()

    def dispatch_request(self, *args, **kwargs):
        if self.form is not None:
            self.processed_form = self.process_form(self.form)
        self.process_request(*args, **kwargs)
        if self.response_values:
            self.response_values['status'] = 'ok'
            return jsonify(self.response_values)
        return '', 200

    def process_form(self, form):
        if request.content_type == 'application/json':
            raw_data = request.get_json()
            raw_data.update(request.files)
            raw_data.update(request.args)
            processed_form = form.from_json(raw_data)
        else:
            raw_data = CombinedMultiDict((request.args, request.files, request.form))
            processed_form = form(raw_data)
        if not processed_form.validate():
            raise ValidationError(processed_form.errors)
        return processed_form


class BaseMethodView(BaseView):
    def __init__(self):
        super(BaseMethodView, self).__init__()

    def process_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)

        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)

        assert meth is not None, 'Unimplemented method %r' % request.method
        return meth(*args, **kwargs)
