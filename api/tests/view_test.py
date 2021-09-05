
from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.

User = get_user_model()


class MeetingRoomTestCase(TestCase):
    create_room_url = '/api/rooms/create/'
    get_all_rooms_url = '/api/rooms/'
    create_reservation_url = '/api/reservations/create/'
    create_employee_url = '/api/users/register/'
    login_url = "/api/login/"

    def setUp(self):
        user_a = self.client.post(self.create_employee_url, {"first_name": "John", "last_name": "Doe",
                                  "email": "johndoe@email.com", "password": "password123"}, follow=True)
        user_b = self.client.post(self.create_employee_url, {"first_name": "Tom", "last_name": "Moe",
                                  "email": "tommoe@email.com", "password": "password123"}, follow=True)

        data_a = {"username": "johndoe@email.com",
                  "password": "password123"}

        data_b = {"username": "tommoe@email.com",
                  "password": "password123"}

        response_user_a = self.client.post(self.login_url, data_a, follow=True)
        response_user_b = self.client.post(self.login_url, data_b, follow=True)
        self.access_token_user_a = response_user_a.data['access']
        self.access_token_user_b = response_user_b.data['access']
        self.user_a = user_a

        response = self.client.post(
            self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_b}')
        self.assertEqual(response.status_code, 201)

    def test_authorized_employee_list_all_rooms(self):
        response = self.client.get(
            self.get_all_rooms_url,  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(len(response.data), 2)

    def test_authorized_employee_get_room(self):
        response = self.client.get(
            '/api/rooms/1/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(response.status_code, 200)

    def test_authorized_employee_reservation_create(self):
        response = self.client.post(
            self.create_reservation_url, {
                "title": "reservation1",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2021-09-03T14:07:10",
                "room": 1,
                "employees": [1, 2]
            }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')

        self.assertEqual(response.status_code, 200)

    def test_not_authorized_employee_reservation_create(self):
        response = self.client.post(
            self.create_reservation_url, {
                "title": "reservation1",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2021-09-03T14:07:10",
                "room": 1,
                "employees": [1, 2]
            })

        self.assertEqual(response.status_code, 401)


class ReservationTestCase(TestCase):
    create_room_url = '/api/rooms/create/'
    get_all_rooms_url = '/api/rooms/'
    create_reservation_url = '/api/reservations/create/'
    create_employee_url = '/api/users/register/'
    login_url = "/api/login/"

    def setUp(self):

        user_a = self.client.post(self.create_employee_url, {"first_name": "John", "last_name": "Doe",
                                                             "email": "johndoe@email.com", "password": "password123"}, follow=True)
        user_b = self.client.post(self.create_employee_url, {"first_name": "Tom", "last_name": "Moe",
                                                             "email": "tommoe@email.com", "password": "password123"}, follow=True)

        data_a = {"username": "johndoe@email.com",
                  "password": "password123"}

        data_b = {"username": "tommoe@email.com",
                  "password": "password123"}

        response_user_a = self.client.post(self.login_url, data_a, follow=True)
        response_user_b = self.client.post(self.login_url, data_b, follow=True)
        self.access_token_user_a = response_user_a.data['access']
        self.access_token_user_b = response_user_b.data['access']
        self.user_a = user_a

        response = self.client.post(
            self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            self.create_reservation_url, {
                "title": "reservation1",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2022-09-03T14:07:10",
                "room": 1,
                "employees": [1, 2]
            }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        response = self.client.post(
            self.create_reservation_url, {
                "title": "reservation2",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2021-09-03T14:07:10",
                "room": 1,
                "employees": [1, 2]
            }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

    def test_authorized_employee_get_meeting_room_reservations(self):
        response = self.client.get(
            '/api/rooms/1/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')

        reservations = response.data['reservations']
        self.assertEqual(len(reservations), 1)

    def test_authorized_employee_get_room_reservations_filtered_by_name(self):
        response = self.client.get(
            '/api/rooms/1/?keyword=tom',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')

        filtered_reservations = response.data['reservations']
        self.assertEqual(len(filtered_reservations), 0)

    def test_authorized_employee_list_all_employees(self):
        response = self.client.get(
            '/api/users/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')

        self.assertEqual(len(response.data), 2)

    def test_authorized_employee_list_all_employee_reservations(self):
        response = self.client.get(
            '/api/users/1/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(len(response.data), 1)

    def test_authorized_employee_not_creator_reservation_cancel(self):
        response = self.client.delete(
            '/api/reservations/delete/1/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_b}')
        self.assertEqual(response.status_code, 400)

    def test_not_authorized_employee_reservation_cancel(self):
        response = self.client.delete(
            '/api/reservations/delete/1/')
        self.assertEqual(response.status_code, 401)

    def test_authorized_employee_reservation_cancel(self):
        response = self.client.delete(
            '/api/reservations/delete/1/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(response.status_code, 200)
