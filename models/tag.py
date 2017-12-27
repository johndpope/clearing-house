from datetime import datetime

from db import get_db

from .base import JsonSerializable

db = get_db()


class Tag(db.Model, JsonSerializable):
    max_serialization_depth = 2
    serializable_columns = [
        'name', 'content',
    ]
    name = db.Column(db.String, unique=True, primary_key=True)
    content = db.Column(db.JSON)

    def __repr__(self):
        return '<Tag %r>' % self.name
