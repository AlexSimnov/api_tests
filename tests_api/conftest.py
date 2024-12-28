import pytest
from faker import Faker
import requests

from .constants import BASE_URL, HEADERS

faker = Faker()


@pytest.fixture(scope='session')
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    responce = requests.post(
        f'{BASE_URL}/auth',
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )

    assert responce.status_code == 200, 'Auth Reject'

    token = responce.json().get('token')

    assert token is not None, 'No token in responce'

    session.headers.update({'Cookie': f'token={token}'})

    return session


@pytest.fixture
def booking_data():
    return {
        "firstname": faker.unique.first_name(),
        "lastname": faker.unique.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }


@pytest.fixture
def create_booking(booking_data, auth_session):
    responce = auth_session.post(
        f'{BASE_URL}/booking',
        json=booking_data
    )

    return {'id': responce.json()['bookingid'],
            'old_data': responce.json()['booking']}
