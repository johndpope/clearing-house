from wtforms import FieldList, FormField, StringField, validators

from models import EventState, Tag

from ..base_form import (BaseForm, BaseWithRawForm, JSONField,
                         ListFromTableValidator, OptionalButNotEmptyValidator)
from ..outcome.form import NewOutcomeForm, RestrictedEditOutcomeForm


class NewEventForm(BaseForm):
    content = JSONField(
        'Event content',
        validators=[validators.DataRequired()]
    )
    outcomes = FieldList(
        FormField(NewOutcomeForm, 'Possible outcomes'),
        validators=[validators.DataRequired()]
    )
    tags = FieldList(StringField('Tag', validators=[
        validators.DataRequired(),
        ListFromTableValidator(Tag, 'name'),
    ]))


class EditEventForm(BaseForm):
    content = JSONField(
        'Event content',
        validators=[
            OptionalButNotEmptyValidator(),
        ],
    )
    outcomes = FieldList(
        FormField(RestrictedEditOutcomeForm, 'Possible outcomes'),
        validators=[
            OptionalButNotEmptyValidator(),
        ],
    )
    state = StringField(
        'State',
        validators=[
            OptionalButNotEmptyValidator(),
            validators.AnyOf([e.name for e in EventState])
        ]
    )
    tags = FieldList(
        StringField(
            'Tag',
            validators=[
                OptionalButNotEmptyValidator(),
                ListFromTableValidator(Tag, 'name'),
            ]
        ),
        validators=[
            OptionalButNotEmptyValidator(),
        ]
    )


class EventsForm(BaseWithRawForm):
    state = FieldList(
        StringField(
            'State',
            validators=[
                validators.AnyOf([e.name for e in EventState])
            ],
        ),
        validators=[
            OptionalButNotEmptyValidator(),
        ]
    )
