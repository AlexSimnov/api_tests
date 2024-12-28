import pytest
from tests_api.constants import BASE_URL

from http import HTTPStatus


class TestBooking:
    def test_create_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f'{BASE_URL}/booking',
                                           json=booking_data)

        assert create_booking.status_code == 200, 'Ошибка при создании брони'

        booking_id = create_booking.json().get('bookingid')

        assert booking_id is not None, 'Идентификатор брони не обнаружен'

        assert create_booking.json()['booking']['firstname'] == booking_data['firstname'], (
            'Заданное имя не совпадает'
        )

        assert create_booking.json()['booking']['totalprice'] == booking_data['totalprice'], (
            'Заданная стоимость не совпадает'
        )

        get_booking = auth_session.get(f'{BASE_URL}/booking/{booking_id}')

        assert get_booking.status_code == 200, 'Бронь не найдена'

        assert get_booking.json()['lastname'] == booking_data['lastname'], (
            'Заданная фамилия не найдена'
        )

        delete_booking = auth_session.delete(f'{BASE_URL}/booking/{booking_id}')

        assert delete_booking.status_code == 201, (
            'Бронь не удалась'
        )

    def test_negative_post_booking(self, auth_session, booking_data):

        booking_data.update({'totalprice': 'total'})

        post_booking = auth_session.post(
            f'{BASE_URL}/booking',
            json=booking_data)

        assert post_booking.status_code == HTTPStatus.BAD_REQUEST

    def test_put_booking(self, create_booking, booking_data, auth_session):

        data = {
            "firstname": 'Jake',
            "lastname": 'Makmilan',
            "totalprice": 1001,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Cigars"
        }

        put_booking = auth_session.put(
            f'{BASE_URL}/booking/{create_booking['id']}',
            json=data
        )

        assert put_booking.status_code == HTTPStatus.OK, 'Ошибка при обновлении брони'

        assert put_booking.json() != create_booking['old_data']

    def test_patch_booking(self, create_booking, booking_data, auth_session):

        booking_data.update({'firstname': 'James'})

        patch_booking = auth_session.put(
            f'{BASE_URL}/booking/{create_booking['id']}',
            json=booking_data
        )

        assert patch_booking.status_code == HTTPStatus.OK, 'Ошибка при обновлении брони'

        assert patch_booking.json()['firstname'] == 'James', 'Ошибка, имя не обновилось'
        assert patch_booking.json()['firstname'] != create_booking['old_data']['firstname'], 'Ошибка, данные не обновились'
