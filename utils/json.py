from __future__ import absolute_import

import json


class ExploitableJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'as_dict'):
            return o.as_dict()
        elif isinstance(o, (bytes, bytearray)):
            return o.decode('utf-8')
        else:
            return super().default(o)
