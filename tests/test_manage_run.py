from webapp.app import app
from webapp.forms import ManageRunForm
import pytest


@pytest.fixture()
def client():
    """The flask test client for our app.

    This lets us trigger http requests to end points without needing a server running.
    """

    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()


    return client


def test_manage_run_get_no_run_id(client):

    res = client.get('/reference')
    assert res.status_code == 404


def test_manage_run_get_valid_run_id(client):

    res = client.get('/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert res.status_code == 200
    assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data


def test_manage_run_get_invalid_run_id(client):

    res = client.get('/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d0')
    assert res.status_code == 404
    assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' not in res.data


def test_manage_run_press_edit_data(client):

    with app.test_request_context():
        # Setup form submission information
        selection = ManageRunForm.edit_button
        data = {'edit_button': 'True'}
        # Post to weights with valid form data
        res = client.post('/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

    # Ensure redirect target found
    assert res.status_code == 302
    # Ensure redirecting
    assert b'Redirecting' in res.data
    # Ensure target is weights_2
    assert b'/new_run_1' in res.data
    # Ensure validation passed
    assert b'This field is required.' not in res.data


def test_manage_run_press_display_weights(client):

    with app.test_request_context():
        # Setup form submission information
        selection = ManageRunForm.display_button
        data = {'display_button': 'True'}
        # Post to weights with valid form data
        res = client.post('/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

    # Ensure redirect target found
    assert res.status_code == 302
    # Ensure redirecting
    assert b'Redirecting' in res.data
    # Ensure target is weights_2
    assert b'/weights' in res.data
    # Ensure validation passed
    assert b'This field is required.' not in res.data


def test_manage_run_press_manage_run_tab(client):

    with app.test_request_context():
        # Setup form submission information
        selection = ManageRunForm.edit_button
        data = {'manage_run_button': 'True'}
        # Post to weights with valid form data
        res = client.post('/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

    # Ensure redirect target found
    assert res.status_code == 302
    # Ensure redirecting
    assert b'Redirecting' in res.data
    # Ensure target is weights_2
    assert b'/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data
    # Ensure validation passed
    assert b'This field is required.' not in res.data


def test_manage_run_press_export_tab(client):

    with app.test_request_context():
        # Setup form submission information
        selection = ManageRunForm.edit_button
        data = {'export_button': 'True'}
        # Post to weights with valid form data
        res = client.post('/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

    # Ensure redirect target found
    assert res.status_code == 302
    # Ensure redirecting
    assert b'Redirecting' in res.data
    # Ensure target is weights_2
    assert b'/export_data/9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data
    # Ensure validation passed
    assert b'This field is required.' not in res.data


@pytest.mark.skip(reason="Functionality Not Implemented.")
def test_manage_run_press_run_selected(client):
    with app.test_request_context():
        # Setup form submission information
        selection = ManageRunForm.run_button
        data = {'run_button': 'True'}
        # Post to weights with valid form data
        res = client.post('/reference/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

    # Functionality has yet be be set up
    assert False