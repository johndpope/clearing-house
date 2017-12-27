import datetime
import enum
import time

from db import get_db

from .base import JsonSerializable

db = get_db()


tags = db.Table('tags',
    db.Column('tag_name', db.String, db.ForeignKey('tag.name'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)


class EventState(enum.IntEnum):
    preparing = 0
    ongoing = 1
    holding = 2
    clearing = 3
    ended = 4
    deleted = 5


class Event(db.Model, JsonSerializable):
    max_serialization_depth = 2
    serializable_columns = [
        'id', 'content', 'outcomes',
        'create_timestamp', 'event_timestamp',
        'tags', 'state',
    ]

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.JSON)
    create_timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.datetime.fromtimestamp(time.time())
    )
    event_timestamp = db.Column(db.DateTime)
    outcomes = db.relationship('Outcome', backref='event', lazy=False)
    bitcoin_private_key = db.Column(db.String, nullable=False, unique=True, )
    bitcoin_public_key = db.Column(db.String, nullable=False,)
    bitcoin_address = db.Column(db.String, nullable=False, unique=True,)

    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('events', lazy=True))
    state = db.Column(db.Enum(EventState), nullable=False, default=EventState.preparing)

    def __repr__(self):
        return '<Event %r>' % self.id
