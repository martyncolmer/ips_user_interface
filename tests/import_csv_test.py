import os
from webapp import app
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_new_run_3(self):
        res = self.app.get('/new_run_3')
        assert b'File type accepted is .csv' in res.data

if __name__ == '__main__':
    unittest.main()