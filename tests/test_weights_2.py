from webapp.app import app
import pytest
from flask import session


@pytest.fixture()
def client():
    """The flask test client for our app.

    This lets us trigger http requests to end points without needing a server running.
    """

    app.testing = True
    client = app.test_client()

    return client


def test_weights_2_get(client):
    res = client.get('/weights_2')
    assert res.status_code == 404

    res = client.get('/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/0')
    assert b'Portroute' in res.data
    assert b'Weekday' in res.data
    assert b'Arrivedepart' in res.data
    assert b'Am Pm Night' in res.data
    assert b'Total' in res.data
    assert res.status_code == 200

    # Incorrect data source
    res = client.get('/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/10')
    assert b'No Records to show...' in res.data
    assert b'Shift Data' in res.data
    assert res.status_code == 200

    # Incorrect run id
    res = client.get('/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a6d011e/SHIFT_DATA/Shift Data/0')
    assert b'No Records to show...' in res.data
    assert b'Shift Data' in res.data
    assert res.status_code == 200

    # Incorrect table name
    res = client.get('/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/FAKE_TABLE/Shift Data/0')
    assert b'No Records to show...' in res.data
    assert res.status_code == 200


def test_weights_2_post(client):

    # Ensure redirect happens when post with ID is executed
    res = client.post('/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    assert res.status_code == 302
    res = client.post('/weights_2/0000')
    assert res.status_code == 302

    pass
    # Export redirect functionality will be added once target is established

