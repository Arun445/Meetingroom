from api.views import cancel_reservation
from django.conf import settings
from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


# Create your tests here.

User = get_user_model()


class UserTestCase(TestCase):
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

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_user_full_name(self):
        full_name = self.user_a.data['full_name']
        self.assertEqual(full_name, 'John Doe')

    def test_username(self):
        full_name = self.user_a.data['username']
        self.assertEqual(full_name, self.user_a.data['email'])

    def test_user_create_room(self):
        response = self.client.post(
            self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(
            self.create_room_url, {"name": "ROOM2"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_b}')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(
            self.get_all_rooms_url,  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
        self.assertEqual(len(response.data), 2)


class AuthorizationTestCase(TestCase):
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


def test_authorized_employee_reservation_cancel(self):

    self.client.post(
        self.create_reservation_url, {
            "title": "reservation1",
            "reserved_from": "2021-09-02T14:07:09",
            "reserved_to": "2022-09-03T14:07:10",
            "room": 1,
            "employees": [1, 2]
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')

    response = self.client.delete(
        '/api/reservations/delete/1/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_b}')

    self.assertEqual(response.status_code, 400)

    response = self.client.delete(
        '/api/reservations/delete/1/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')

    self.assertEqual(response.status_code, 200)


def test_not_authorized_employee_reservation_cancel(self):
    self.client.post(
        self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')
    self.client.post(
        self.create_reservation_url, {
            "title": "reservation1",
            "reserved_from": "2021-09-02T14:07:09",
            "reserved_to": "2022-09-03T14:07:10",
            "room": 1,
            "employees": [1, 2]
        }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}')

    response = self.client.delete(
        '/api/reservations/delete/1/')

    self.assertEqual(response.status_code, 401)
