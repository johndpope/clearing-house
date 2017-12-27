import enum

from db import get_db

from .base import JsonSerializable

db = get_db()


class OutcomeState(enum.Enum):
    default = 0
    loser = 1
    winner = 2


class Outcome(db.Model, JsonSerializable):
    serializable_columns = ['id', 'content', 'bitcoin_address', 'state']

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False,)
    content = db.Column(db.JSON)
    bitcoin_private_key = db.Column(db.String, nullable=False, unique=True, )
    bitcoin_public_key = db.Column(db.String, nullable=False,)
    bitcoin_address = db.Column(db.String, nullable=False, unique=True,)

    state = db.Column(db.Enum(OutcomeState), nullable=False, default=OutcomeState.default)

    def __repr__(self):
        return '<Outcome %r>' % self.name
