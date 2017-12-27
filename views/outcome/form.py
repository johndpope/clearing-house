from wtforms import IntegerField, StringField, validators

from models import OutcomeState

from ..base_form import BaseForm, JSONField, OptionalButNotEmptyValidator


class NewOutcomeForm(BaseForm):
    content = JSONField('Outcome content', validators=[validators.DataRequired()])


class RestrictedEditOutcomeForm(BaseForm):
    id = IntegerField('Outcome ID', validators=[validators.DataRequired()])
    content = JSONField('Outcome content', validators=[OptionalButNotEmptyValidator()])


class EditOutcomeForm(BaseForm):
    content = JSONField('Outcome content', validators=[OptionalButNotEmptyValidator()])
    state = StringField(
        'State',
        validators=[
            OptionalButNotEmptyValidator(),
            validators.AnyOf([e.name for e in OutcomeState])
        ]
    )
