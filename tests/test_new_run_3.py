import pytest
from webapp.forms import LoadDataForm
from werkzeug.datastructures import FileStorage
import webapp as web

app = web.create_app()

@pytest.fixture()
def test_client():
    """The flask test client for this page.
    Using this, HTML pages can be tested without a live server.
    """

    app.testing = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    return client


# Test that the standard page renders correctly.
def test_new_run_3(test_client):
    res = test_client.get('/new_run/new_run_3')
    assert res.status_code == 200
    assert b'File type accepted is .csv' in res.data


# Test that no error messages display when first seeing the basic page.
def test_no_errors_new_run_3(test_client):
    res = test_client.get('/new_run/new_run_3')
    assert b'This field is required.' not in res.data
    assert b'All fields must be filled with .csv files only.' not in res.data


# TODO: ensure that the test gives the expected number of these error messages
# Test that an error is displayed if no files are given.
def test_missing_files_error_new_run_3(test_client):
    res = test_client.post('/new_run/new_run_3')
    assert res.status_code == 200
    assert b'This field is required.' in res.data


# Test that the error is not displayed if all files are given.
def test_no_error_new_run_3_files(test_client):
    # Given
    with app.test_request_context():
        dummy_file = FileStorage(filename='data.csv')
        form = LoadDataForm(survey_file=dummy_file,
                            shift_file=dummy_file,
                            non_response_file=dummy_file,
                            unsampled_file=dummy_file,
                            tunnel_file=dummy_file,
                            sea_file=dummy_file,
                            air_file=dummy_file)

        res = test_client.post('/new_run/new_run_3', data=form.data, follow_redirects=True)
    assert res.status_code == 200
    assert b'Select process variables' in res.data
