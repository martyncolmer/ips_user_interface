import pytest
from webapp.forms import LoadDataForm
from werkzeug.datastructures import FileStorage
import webapp as web



def get_client_and_app():
    """The flask test client for this page.
    Using this, HTML pages can be tested without a live server.
    """
    app = web.create_app()
    app.testing = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()

    return client, app


# Test that an error is displayed if no files are given.
@pytest.mark.skip
def test_missing_files_error_new_run_3():

    client, app = get_client_and_app()
    res = client.post('/new_run/new_run_3')
    assert res.status_code == 200
    assert b'This field is required.' in res.data


@pytest.mark.skip
def test_wrong_files_error_new_run_3():
    client, app = get_client_and_app()
    with app.test_request_context():
        dummy_file = FileStorage(filename='data.txt')
        form = LoadDataForm(survey_file=dummy_file,
                            shift_file=dummy_file,
                            non_response_file=dummy_file,
                            unsampled_file=dummy_file,
                            tunnel_file=dummy_file,
                            sea_file=dummy_file,
                            air_file=dummy_file)

        res = client.post('/new_run/new_run_3', data=form.data, follow_redirects=True)
    assert res.status_code == 200
    assert b'This field is required.' in res.data
    assert b'Select process variables' not in res.data


# Test that the error is not displayed if all files are given.
@pytest.mark.skip
def test_no_error_new_run_3_files():
    client, app = get_client_and_app()
    with app.test_request_context():
        dummy_file = FileStorage(filename='data.csv')
        form = LoadDataForm(survey_file=dummy_file,
                            shift_file=dummy_file,
                            non_response_file=dummy_file,
                            unsampled_file=dummy_file,
                            tunnel_file=dummy_file,
                            sea_file=dummy_file,
                            air_file=dummy_file)

        res = client.post('/new_run/new_run_3', data=form.data, follow_redirects=True)
    assert res.status_code == 200
    assert b'Select process variables' in res.data
