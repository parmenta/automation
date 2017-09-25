import json
import pytest
from crud_rest import app

@pytest.fixture
def client(request):
    test_client = app.test_client()

    return test_client

def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

@pytest.mark.xfail
def test_getAll(client):
    response = client.get('/getAll')
    assert response.status_code == 200
    assert json_of_response(response) == {'result': [{'activity': 'add test', 'date_created': 'Sun, 24 Sep 2017 17:54:50 GMT', 'name': 'Caro', 'status': 'CLOSE'},
                                                     {'activity': 'add test', 'date_created': 'Sun, 24 Sep 2017 17:59:06 GMT', 'name': 'Paula', 'status': 'CLOSE'}]}
def test_add(client):
    response = post_json(client, '/add', {'name': 'Paula', 'activity': 'add test','status' : 'CLOSE'})
    assert response.status_code == 200
    assert json_of_response(response) == {'result': {'name': 'Paula', 'activity': 'add test','status' : 'CLOSE'}}

def test_get_name(client):
    response = client.get('/get/Paula')
    assert response.status_code == 200
    assert json_of_response(response) == {'result': {'activity': 'add test', 'date_created': 'Sun, 24 Sep 2017 17:58:57 GMT', 'name': 'Paula', 'status': 'CLOSE'}}
