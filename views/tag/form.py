from wtforms import StringField, validators

from ..base_form import (BaseForm, BaseWithRawForm, JSONField,
                         OptionalButNotEmptyValidator)


class NewTagForm(BaseForm):
    name = StringField('Tag name', validators=[validators.DataRequired()])
    content = JSONField('Event content', validators=[validators.DataRequired()])


class EditTagForm(BaseForm):
    content = JSONField('Event content', validators=[OptionalButNotEmptyValidator()])


class TagForm(BaseWithRawForm):
    pass
