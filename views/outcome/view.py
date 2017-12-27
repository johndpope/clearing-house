from exceptions import InvalidEventStateError, NonexistentEntityError

from db import get_db
from models import EventState, Outcome, OutcomeState

from ..base_view import BaseView
from .form import EditOutcomeForm


class BaseOutcomeView(BaseView):
    valid_event_states = {
        OutcomeState.default: {EventState.holding},
        OutcomeState.loser: {EventState.holding},
        OutcomeState.winner: {EventState.holding},
    }

    def get_by_id(self, outcome_id):
        outcome = Outcome.query.get(outcome_id)
        if not outcome:
            raise NonexistentEntityError(Outcome, outcome_id)
        return outcome

    def change_state(self, outcome, processed_form):
        if not processed_form.state.is_missing:
            new_state = OutcomeState[processed_form.state.data]
            if outcome.event.state not in self.valid_event_states[new_state]:
                raise InvalidEventStateError(new_state.name, outcome.event.state.name)
            outcome.state = new_state


class EditOutcomeView(BaseOutcomeView):
    form = EditOutcomeForm

    def process_request(self, outcome_id):
        outcome = self.get_by_id(outcome_id)
        self.change_state(outcome, self.processed_form)
        get_db().session.commit()
