
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
        # Sets up the testing ground by creating two users and two meeting rooms
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
        self.user_a_id = user_a.data['id']
        self.user_b_id = user_a.data['id']

        response = self.client.post(
            self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        self.room_a_id = response.data['id']

        response = self.client.post(
            self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_b}')

    def test_authorized_employee_list_all_rooms(self):
        # test if an authorized employee can get a list of all rooms
        response = self.client.get(
            self.get_all_rooms_url,  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')
        self.assertEqual(len(response.data), 2)

    def test_authorized_employee_view_room(self):
        # test if an authorized employee can get a specific room with all its reservations
        response = self.client.get(
            f'/api/rooms/{self.room_a_id}/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_authorized_employee_reservation_create(self):
        # test if an authorized employee can create a reservation in a room
        response = self.client.post(
            self.create_reservation_url, {
                "title": "reservation1",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2021-09-03T14:07:10",
                "room": self.room_a_id,
                "employees": [self.user_a_id, self.user_b_id]
            }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_not_authorized_employee_reservation_create(self):
        # test if a not authorized employee can't create a reservation
        response = self.client.post(
            self.create_reservation_url, {
                "title": "reservation1",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2021-09-03T14:07:10",
                "room": self.room_a_id,
                "employees": [self.user_a_id, self.user_b_id]
            })

        self.assertEqual(response.status_code, 401)


class ReservationTestCase(TestCase):
    create_room_url = '/api/rooms/create/'
    get_all_rooms_url = '/api/rooms/'
    create_reservation_url = '/api/reservations/create/'
    create_employee_url = '/api/users/register/'
    login_url = "/api/login/"

    def setUp(self):
        # Sets up the testing ground by creating two users, two meeting rooms and two reservations
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
        self.user_a_id = user_a.data['id']

        response = self.client.post(
            self.create_room_url, {"name": "ROOM1"}, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        self.room_id = response.data['id']

        reservation = self.client.post(
            self.create_reservation_url, {
                "title": "reservation1",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2022-09-03T14:07:10",
                "room": self.room_id,
                "employees": [user_a.data['id'], user_b.data['id']]
            }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        self.client.post(
            self.create_reservation_url, {
                "title": "reservation2",
                "reserved_from": "2021-09-02T14:07:09",
                "reserved_to": "2021-09-03T14:07:10",
                "room": self.room_id,
                "employees": [user_a.data['id'], user_b.data['id']]
            }, HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        self.reservation_id = reservation.data['id']

    def test_authorized_employee_get_meeting_room_reservations(self):
       # test if an authorized employee can get a specific room with all its reservations and also not show invalid reservations
        response = self.client.get(
            f'/api/rooms/{self.room_id}/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        reservations = response.data['reservations']
        self.assertEqual(len(reservations), 1)

    def test_authorized_employee_get_room_reservations_filtered_by_name(self):
        # test if an authorized employee can get a specific room and filter it by an employee
        response = self.client.get(
            f'/api/rooms/{self.room_id}/?keyword=tom',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        filtered_reservations = response.data['reservations']
        self.assertEqual(len(filtered_reservations), 0)

    def test_authorized_employee_list_all_employees(self):
        # test if an authorized employee can get a list of all the employees
        response = self.client.get(
            '/api/users/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')

        self.assertEqual(len(response.data), 2)

    def test_authorized_employee_list_all_employee_reservations(self):
        # test if an authorized employee can check a emplyees reservations and show only the valid ones
        response = self.client.get(
            f'/api/users/{self.user_a_id}/',  HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')
        self.assertEqual(len(response.data), 1)

    def test_authorized_employee_not_creator_reservation_cancel(self):
        # test if an authorized employee but not the author of the reservation, can't cancel a reservation
        response = self.client.delete(
            f'/api/reservations/delete/{self.reservation_id}/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_b}')
        self.assertEqual(response.status_code, 400)

    def test_not_authorized_employee_reservation_cancel(self):
        # test if a not authorized employee can't cancel a reservation
        response = self.client.delete(
            f'/api/reservations/delete/{self.reservation_id}/')
        self.assertEqual(response.status_code, 401)

    def test_authorized_employee_reservation_cancel(self):
        # test if an authorized employee and the author of this reservation can cancel it
        response = self.client.delete(
            f'/api/reservations/delete/{self.reservation_id}/', HTTP_AUTHORIZATION=f'Bearer {self.access_token_user_a}', content_type='application/json')
        self.assertEqual(response.status_code, 200)
