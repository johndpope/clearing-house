import enum
import time
from datetime import date, datetime
from exceptions import UnsupportedLanguageError

from sqlalchemy.inspection import inspect


def process_field(field):
    if isinstance(field, (date, datetime)):
        return int(time.mktime(field.timetuple()))
    if isinstance(field, enum.Enum):
        return field.name
    return field


def process_content(content, lang):
    if 'translates' in content:
        translates = content.pop('translates')
        if lang not in translates:
            raise UnsupportedLanguageError(list(sorted(translates.keys())), lang)
        content.update(translates[lang])


class JsonSerializable:
    max_serialization_depth = 1

    def as_dict(self, depth=0, max_depth=None, except_fields=None, lang=None):
        except_fields = set(except_fields or [])
        if max_depth is None:
            max_depth = self.__class__.max_serialization_depth
        else:
            max_depth = min(max_depth, depth + self.__class__.max_serialization_depth)
        if depth >= max_depth:
            return
        serializable_columns = getattr(self, 'serializable_columns', [])
        columns = self.__table__.columns.keys()
        result_dict = {
            c: process_field(getattr(self, c))
            for c in (serializable_columns or columns)
            if c in columns and c not in except_fields
        }
        if lang and 'content' in result_dict:
            process_content(result_dict['content'], lang)

        for rel in inspect(self.__class__).relationships.keys():
            if serializable_columns and rel not in serializable_columns:
                continue
            attr = getattr(self, rel)
            if isinstance(attr, list):
                attr = list(
                    filter(
                        lambda x: x is not None,
                        map(
                            lambda x: x.as_dict(depth=depth + 1, max_depth=max_depth, lang=lang),
                            attr,
                        ),
                    )
                )
            else:
                attr = attr.as_dict(depth=depth + 1, max_depth=max_depth, lang=lang)
            if attr:
                result_dict[rel] = attr
        return result_dict
