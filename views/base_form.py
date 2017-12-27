import json

import wtforms_json
from flask_wtf import FlaskForm
from wtforms import IntegerField, ValidationError, fields, validators
from wtforms.widgets import TextArea

wtforms_json.init()


class BaseForm(FlaskForm):
    pass


class BaseWithRawForm(FlaskForm):
    raw = IntegerField('Raw', validators=[validators.Optional(), validators.AnyOf([0, 1])])


class JSONField(fields.Field):
    widget = TextArea()

    def _value(self):
        return self.data

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                if isinstance(valuelist[0], dict):
                    self.data = valuelist[0]
                else:
                    self.data = json.loads(valuelist[0])
            except ValueError:
                raise ValueError('This field contains invalid JSON')
        else:
            self.data = None

    def pre_validate(self, form):
        super().pre_validate(form)
        if self.data:
            try:
                json.dumps(self.data)
            except TypeError:
                raise ValueError('This field contains invalid JSON')


class ListFromTableValidator:
    def __init__(self, model, column_name):
        self.values_callable = lambda: set(map(
            lambda x: getattr(x, column_name),
            model.query.distinct(getattr(model, column_name))
        ))

    def __call__(self, form, field):
        values = self.values_callable()
        if field.data not in values:
            raise ValidationError('Invalid value, must be one of: %s.' % ', '.join(sorted(values)))


class OptionalButNotEmptyValidator:
    """
    Allows missing but not empty input and stops the validation chain from continuing.
    """
    field_flags = ('optional', )

    def __call__(self, form, field):
        if not field.raw_data:
            raise validators.StopValidation()
