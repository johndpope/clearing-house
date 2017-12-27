from exceptions import InvalidStateTransitionError, NonexistentEntityError

from coins.btc import get_btc
from db import get_db
from models import Event, EventState, Outcome, Tag

from ..base_form import BaseWithRawForm
from ..base_view import BaseView
from .form import EditEventForm, EventsForm, NewEventForm


class BaseEventView(BaseView):
    valid_transitions = {
        EventState.preparing: {EventState.preparing, EventState.ongoing, EventState.deleted},
        EventState.ongoing: {EventState.ongoing, EventState.holding},
        EventState.holding: {EventState.holding, EventState.clearing},
        EventState.clearing: {EventState.clearing, EventState.ended},
        EventState.ended: {EventState.ended, EventState.deleted},
        EventState.deleted: {EventState.deleted},
    }

    def get_by_id(self, event_id):
        event = Event.query.get(event_id)
        if not event or event.state == EventState.deleted:
            raise NonexistentEntityError(Event, event_id)
        return event

    def change_tags(self, event, processed_form):
        if not processed_form['tags'].is_missing:
            tag_names = [tag.data for tag in processed_form.tags.entries]
            event.tags = list(Tag.query.filter(Tag.name.in_(tag_names)))

    def change_state(self, event, processed_form):
        if not processed_form['state'].is_missing:
            old_state = EventState(event.state)
            new_state = EventState[processed_form['state'].data]
            if new_state not in self.valid_transitions[old_state]:
                raise InvalidStateTransitionError(old_state.name, new_state.name)
            event.state = EventState[processed_form['state'].data].value


class EventView(BaseEventView):
    form = BaseWithRawForm

    def process_request(self, event_id):
        event = self.get_by_id(event_id)
        event = event.as_dict(lang=self.raw_aware_lang)
        for outcome in event['outcomes']:
            outcome['balance'] = get_btc().get_balance(outcome['bitcoin_address'])
        self.response_values.update({
            'event': event
        })


class EditEventView(BaseEventView):
    form = EditEventForm

    def process_request(self, event_id):
        event = self.get_by_id(event_id)
        self.change_state(event, self.processed_form)
        self.change_tags(event, self.processed_form)
        if not self.processed_form['content'].is_missing:
            event.content = self.processed_form['content'].data
        for outcome in self.processed_form['outcomes'].entries:
            outcome_entity = Outcome.query.get(outcome['id'].data)
            if not outcome_entity:
                raise NonexistentEntityError(Outcome, outcome['id'])
            if not outcome['content'].is_missing:
                outcome_entity.content = outcome['content'].data
        get_db().session.commit()


class EventsView(BaseEventView):
    form = EventsForm

    def get_events(self, *args, **kwargs):
        return Event.query

    def process_request(self, *args, **kwargs):
        events = self.get_events(*args, **kwargs).filter(
            Event.state != EventState.deleted
        ).order_by(
            Event.create_timestamp.desc(),
        )
        if not self.processed_form.state.is_missing:
            events = events.filter(
                Event.state.in_(self.processed_form['state'].data)
            )
        events = list(
            map(
                lambda x: x.as_dict(max_depth=2, lang=self.raw_aware_lang),
                events.all()
            )
        )
        self.response_values.update({
            'events': events,
        })


class EventsByTagView(EventsView):
    def get_events(self, tag_name, *args, **kwargs):
        return Event.query.filter(Event.tags.any(name=tag_name))


class NewEventView(BaseEventView):
    form = NewEventForm

    def process_request(self):
        intermediate_private_key = get_btc().create_private_key()
        event = Event(
            content=self.processed_form.content.data,
            bitcoin_private_key=intermediate_private_key.to_compressed_wif(),
            bitcoin_public_key=intermediate_private_key.get_public_key().to_hex(),
            bitcoin_address=intermediate_private_key.get_address().to_wif(),
        )
        self.change_tags(event, self.processed_form)
        get_db().session.add(event)
        get_db().session.flush()
        for outcome in self.processed_form.outcomes.entries:
            private_key = get_btc().create_private_key()
            get_db().session.add(
                Outcome(
                    event_id=event.id,
                    content=outcome.content.data,
                    bitcoin_private_key=private_key.to_compressed_wif(),
                    bitcoin_public_key=private_key.get_public_key().to_hex(),
                    bitcoin_address=private_key.get_address().to_wif(),
                )
            )
        get_db().session.commit()
