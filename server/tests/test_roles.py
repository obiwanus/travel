import pytest
import requests


def api_url(url):
    return 'http://localhost:8000/api%s' % url


class Session:

    def __init__(self, email, password):
        self.session = requests.session()
        login = self.session.post(api_url('/login/'), {
            'email': email,
            'password': password,
        })
        assert login.status_code == 200
        response = self.session.get(api_url('/csrf/token/'))
        self.csrf_token = response.json().get('csrfmiddlewaretoken')
        assert self.csrf_token is not None

    def get(self, url):
        return self.session.get(api_url(url))

    def post(self, url, data):
        return self.session.post(api_url(url), json=data, headers={
            'X-CSRFToken': self.csrf_token,
        })

    def delete(self, url):
        return self.session.delete(api_url(url), headers={
            'X-CSRFToken': self.csrf_token,
        })

    def put(self, url):
        return self.session.put(api_url(url), json=data, headers={
            'X-CSRFToken': self.csrf_token,
        })



@pytest.fixture
def normal():
    return Session('normal@test.com', 'pqlapqlapqla')


@pytest.fixture
def manager():
    return Session('user-manager@test.com', 'pqlapqlapqla')


@pytest.fixture
def admin():
    return Session('user-manager@test.com', 'pqlapqlapqla')


def assert_can_view_trips(session):
    response = session.get('/trips/')
    assert response.status_code == 200
    assert 'trips' in response.json()


def test_every_role_can_view_trips(normal, manager, admin):
    assert_can_view_trips(normal)
    assert_can_view_trips(manager)
    assert_can_view_trips(admin)


def add_test_trip_as(session):
    response = session.post('/trips/', {
        'trip': {
            'destination': 'Test destination',
            'start_date': '2017-07-20',
            'end_date': '2017-11-23',
            'comment': 'hopefully this will be deleted',
        }
    })
    assert response.status_code == 201
    assert 'trip' in response.json()
    return response


def delete_test_trip_as(session, trip_id):
    return session.delete('/trips/%s/' % trip_id)


def test_user_can_add_and_delete_trips(normal):
    response = add_test_trip_as(normal)
    trip_id = response.json()['trip']['id']
    response = delete_test_trip_as(normal, trip_id)
    assert response.status_code == 204


def test_user_cant_delete_other_users_trips(normal, manager):
    response = add_test_trip_as(manager)
    trip_id = response.json()['trip']['id']
    response = delete_test_trip_as(normal, trip_id)
    assert response.status_code == 404
