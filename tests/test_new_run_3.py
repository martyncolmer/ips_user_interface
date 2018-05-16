import os
from webapp import app
import unittest
import tempfile
from webapp.forms import LoadDataForm
from werkzeug.datastructures import FileStorage

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['WTF_CSRF_ENABLED'] = False
        app.testing = True
        self.app = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])


    def test_new_run_3(self):
        res = self.app.get('/new_run_3')
        assert b'File type accepted is .csv' in res.data


    def test_no_errors_new_run_3(self):
        res = self.app.get('/new_run_3')
        assert b'This field is required.' not in res.data


    def test_missing_files_error_new_run_3(self):
        res = self.app.post('/new_run_3')
        assert b'This field is required.' in res.data

    def test_no_error_new_run_3_files(self):
        # Given
        with app.app.test_request_context():
            f = FileStorage(filename='data.csv')
            form = LoadDataForm(survey_file=f,
                                shift_file=f,
                                non_response_file=f,
                                unsampled_file=f,
                                tunnel_file=f,
                                sea_file=f,
                                air_file=f)

            res = self.app.post('/new_run_3', data=form.data)
        assert b'This field is required.' not in res.data

if __name__ == '__main__':
    unittest.main()