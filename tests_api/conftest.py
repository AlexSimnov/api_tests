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
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }
