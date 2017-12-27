from exceptions import ImpossibleBroError, NonexistentEntityError

from db import get_db
from models import Event, Tag

from ..base_form import BaseWithRawForm
from ..base_view import BaseView
from .form import EditTagForm, NewTagForm


class DeleteTagView(BaseView):
    def process_request(self, tag_name, *args, **kwargs):
        tag = Tag.query.get(tag_name)
        if tag is None:
            raise NonexistentEntityError(Tag, tag_name)
        if len(tag.events) != 0:
            raise ImpossibleBroError()
        get_db().session.delete(tag)
        get_db().session.commit()


class EditTagView(BaseView):
    form = EditTagForm

    def process_request(self, tag_name, *args, **kwargs):
        tag = Tag.query.get(tag_name)

        if not self.processed_form.content.is_missing:
            tag.content = self.processed_form.content.data
        get_db().session.commit()


class NewTagView(BaseView):
    form = NewTagForm

    def process_request(self, *args, **kwargs):
        tag = Tag(
            name=self.processed_form.name.data,
            content=self.processed_form.content.data,
        )
        get_db().session.add(tag)
        get_db().session.commit()


class TagsView(BaseView):
    form = BaseWithRawForm

    def process_request(self, *args, **kwargs):
        tags = list(map(lambda x: x.as_dict(max_depth=1, lang=self.raw_aware_lang), Tag.query.all()))
        self.response_values.update({
            'tags': tags
        })
