import pytest
from tests_api.constants import BASE_URL

from http import HTTPStatus


class TestBooking:
    def test_create_booking(self, auth_session, booking_data):
        create_booking = auth_session.post(f'{BASE_URL}/booking',
                                           json=booking_data)

        assert create_booking.status_code == 200, 'Ошибка при создании брони'

        booking_id = create_booking.json().get('booking_id')

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

    def test_patch_booking(self, auth_create_session, booking_data):
        booking_id = auth_create_session.get('booking_id')

        patch_booking = auth_create_session.patch(
            f'{BASE_URL}/booking/{booking_id}',
            json=booking_data
        )

        assert patch_booking.status_code == HTTPStatus.OK

        assert patch_booking.json()['booking_id']['firstname'] == booking_data['firstname']

        get_booking = auth_create_session.get(
            f'{BASE_URL}/booking/{booking_id}'
        )

        assert get_booking.status_code == HTTPStatus.OK

    def test_put_booking(self, auth_create_session, booking_data):
        booking_id = auth_create_session.get('booking_id')

        put_booking = auth_create_session.put(
            f'{BASE_URL}/booking/{booking_id}',
            json={'lastame': booking_data['lastname']}
        )

        assert put_booking.status_code == HTTPStatus.OK

        assert put_booking.json()['booking']['lastname'] == booking_data['lastname']

        get_booking = auth_create_session.get(
            f'{BASE_URL}/booking/{booking_id}'
        )

        assert get_booking.status_code == HTTPStatus.OK

    def test_negative_post_booking(self, auth_session, booking_data):

        post_booking = auth_session.post(
            f'{BASE_URL}/booking',
            json=booking_data.update({'totalprice': 'total'})
        )

        print(booking_data['totalprice'])

        assert post_booking.json()['booking']['totalprice'] == booking_data['totalprice']
