import json

from apps.index import app


def tests_index_status_code_ok():
     client = app.test_client()
     assert client.get('/').status_code == 200


def tests_health_status_ok():
    client = app.test_client()
    assert client.get('/healthz').status_code == 200


def tests_health_body_ok():
    client = app.test_client()
    ret = client.get('/healthz')
    exp = {"status": "ok"}
    assert json.loads(ret.data) == exp
