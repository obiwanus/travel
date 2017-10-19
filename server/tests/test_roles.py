import pytest
import requests


def api_url(url):
    return "http://localhost:8000/api%s" % url


def login_as(email, password):
    session = requests.session()
    login = session.post(api_url("/login/"), {
        "email": email,
        "password": password,
    })
    assert login.status_code == 200
    return session



@pytest.fixture
def normal():
    return login_as("normal@test.com", "pqlapqlapqla")


@pytest.fixture
def manager():
    return login_as("user-manager@test.com", "pqlapqlapqla")


@pytest.fixture
def admin():
    return login_as("user-manager@test.com", "pqlapqlapqla")


def test_can_get_csrf_token():
    response = requests.get(api_url('/csrf/token/'))
    assert response.status_code == 200
    assert 'csrfmiddlewaretoken' in response.json()


def assert_can_view_trips(session):
    response = session.get(api_url("/trips/"))
    assert response.status_code == 200
    assert 'trips' in response.json()


# def test_every_role_can_view_trips(normal, manager, admin):
#     assert_can_view_trips(normal)
#     assert_can_view_trips(manager)
#     assert_can_view_trips(admin)


def test_user_can_add_trips(normal):
    response = normal.post(api_url("/trips/"), {
        'trip': {
            'destination': "Test destination",
            'start_date': '2017-07-20',
            'end_date': '2017-11-23',
            'comment': "hopefully this will be deleted",
        }
    })
    import ipdb; ipdb.set_trace()
    assert response.status_code == 201
    assert 'trip' in response.json()


def test_user_can_delete_trips(normal):
    response = normal.get(api_url("/trips/")).json()
    assert 'trips' in response
    trip_to_delete = None
    for trip in response['trips']:
        if 'test' in trip['destination'].lower():
            trip_to_delete = trip
            break
    assert trip_to_delete is not None
    response = normal.delete(api_url("/trips/%s/" % trip['id']))
    assert response.status_code == 204

