import os
from webapp.app import app
import unittest
import tempfile
from werkzeug.datastructures import FileStorage
from webapp.forms import DataSelectionForm
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


def test_weights_get(client):

    res = client.get('/weights')
    assert res.status_code == 404

    res = client.get('/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert res.status_code == 200
    assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    res = client.get('/weights/0000')
    assert res.status_code == 404
    assert b'Not Found' in res.data


def test_weights_post(client):

    with app.test_request_context():
        # Setup form submission information
        form = DataSelectionForm(data_selection='SHIFT_DATA|Shift Data|0')
        # Post to weights with valid form data
        res = client.post('/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=form.data)

    # Ensure redirect target found
    assert res.status_code == 302
    # Ensure redirecting
    assert b'Redirecting' in res.data
    # Ensure target is weights_2
    assert b'/weights_2' in res.data
    # Ensure validation passed
    assert b'This field is required.' not in res.data

    with app.test_request_context():
        # Setup form submission information
        form = DataSelectionForm(data_selection='')
        # Post to weights with invalid form data
        res = client.post('/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=form.data)

    # Ensure status_code is 200 (OK)
    assert res.status_code == 200
    # Ensure called ID still in res data
    assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data
    # Ensure validation failed
    assert b'This field is required.' in res.data
