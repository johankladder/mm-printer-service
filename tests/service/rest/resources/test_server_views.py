import pytest

from service.rest import app


def test_ping():
    response = app.test_client().get('/server/ping')
    assert response.status_code == 200
    assert response.text == "Pong!"
