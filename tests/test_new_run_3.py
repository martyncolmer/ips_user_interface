from webapp.app import app
import pytest
from webapp.forms import LoadDataForm
from werkzeug.datastructures import FileStorage


@pytest.fixture()
def test_client():
    """The flask test client for this page.
    Using this, HTML pages can be tested without a live server.
    """

    app.testing = True
    client = app.test_client()

    return client


# Test that the standard page renders correctly.
def test_new_run_3(test_client):
    res = test_client.get('/new_run_3')
    assert b'File type accepted is .csv' in res.data


# Test that no error messages display when first seeing the basic page.
def test_no_errors_new_run_3(test_client):
    res = test_client.get('/new_run_3')
    assert b'This field is required.' not in res.data
    assert b'All fields must be filled with .csv files only.' not in res.data


# Test that an error is displayed if no files are given.
def test_missing_files_error_new_run_3(test_client):
    res = test_client.post('/new_run_3')
    assert b'This field is required.' in res.data


# Test that the error is not displayed if all files are given.
def test_no_error_new_run_3_files(test_client):
    # Given
    with app.test_request_context():
        f = FileStorage(filename='data.csv')
        form = LoadDataForm(survey_file=f,
                            shift_file=f,
                            non_response_file=f,
                            unsampled_file=f,
                            tunnel_file=f,
                            sea_file=f,
                            air_file=f)

        res = test_client.post('/new_run_3', data=form.data)
    assert b'This field is required.' not in res.data
