from django.conf import settings
from django.http import response
from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.

User = get_user_model()


class UserTestCase(TestCase):

    def setUp(self):
        user_a = User(username='dummy@gmail.com', email='dummy@gmail.com')
        user_a.first_name = 'dumdumas'
        user_a.last_name = 'dumdum'
        user_a_pw = 'password123'
        self.user_a_pw = user_a_pw
        self.user_a_pw = 'password123'
        self.user_a = user_a
        user_a.set_password(user_a_pw)
        user_a.save()

    def test_user_exists(self):
        user_count = User.objects.all().count()

        self.assertEqual(user_count, 1)
        self.assertNotEqual(user_count, 0)

    def test_user_password(self):

        self.assertTrue(self.user_a.check_password(self.user_a_pw))

    def test_login_url(self):
        login_url = "/api/login/"
        data = {"username": "dummy@gmail.com", 'password': self.user_a_pw}
        self.data = data
        response = self.client.post(login_url, data, folow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_employee_room_create(self):
        self.client.login(username='dummy@gmail.com', password=self.user_a_pw)
        print(self.client)
        response = self.client.post("/api/rooms/create/", {"name": "ROOM1"})
        print(response)
        self.assertTrue(response.status_code == 201)
