import unittest

from app import app
from fixtures.db import DbFixture


class BaseTestView(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app
        self.client = app.test_client()

        self.db = DbFixture(self.app)
        self.db.rollback()
        self.db.commit()

    def tearDown(self):
        self.db.rollback()
