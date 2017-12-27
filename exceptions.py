class BaseError(Exception):
    status_code = 500
    code = 'base_error'
    info = {}

    def as_dict(self):
        return dict(status='error', code=self.code, **self.info)


class ValidationError(BaseError):
    status_code = 400
    code = 'validation_error'

    def __init__(self, errors):
        self.errors = errors
        self.info = {'errors': errors}


class UnsupportedLanguageError(BaseError):
    status_code = 400
    code = 'unsupported_language_error'

    def __init__(self, supported_languages, language):
        self.info = {
            'message': 'Supported languages: {}. Choosen language: {}'.format(supported_languages, language)
        }


class NonexistentEntityError(BaseError):
    status_code = 400
    code = 'nonexistent_entity_error'

    def __init__(self, entity_class, entity_id):
        self.info = {
            'class': entity_class.__name__,
            'id': entity_id,
        }


class InvalidStateTransitionError(BaseError):
    status_code = 400
    code = 'invalid_state_transition_error'

    def __init__(self, source_state, target_state):
        self.info = {
            'source': source_state,
            'target': target_state,
        }


class InvalidEventStateError(BaseError):
    status_code = 400
    code = 'invalid_event_state_error'

    def __init__(self, outcome_state, event_state):
        self.info = {
            'outcome_state': outcome_state,
            'event_state': event_state,
        }


class ImpossibleBroError(BaseError):
    status_code = 400
    code = 'impossible_bro_error'
