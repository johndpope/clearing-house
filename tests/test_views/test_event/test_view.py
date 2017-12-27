import json

from ..base_test_view import BaseTestView
from ..test_data import TEST_EVENTS_VIEW_RESULT, TEST_TAG_SCIENCE_VIEW_RESULT


class TestEventView(BaseTestView):
    def test_event_view(self):
        r = self.client.get('/api/v1/event/', follow_redirects=True)
        self.assertDictEqual(json.loads(r.data), TEST_EVENTS_VIEW_RESULT)

    def test_event_view_by_tag(self):
        r = self.client.get('/api/v1/tag/science', follow_redirects=True)
        self.assertDictEqual(json.loads(r.data), TEST_TAG_SCIENCE_VIEW_RESULT)
