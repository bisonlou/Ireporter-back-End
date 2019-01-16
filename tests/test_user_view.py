import unittest
import json
from api import app, test_client
from api.models.user_model import UserServices


class TestUserView(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = test_client
        self.user_services = UserServices()

        user = {
            'user_name': 'bison',
            'email': 'bisonlou@gmail.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.user_id = message['data']['id']

    def tearDown(self):
        """
        teardown test client
        """
        self.user_services.remove_all()

    def test_register_user_with_blank_password(self):
        """
        Test registering a user without a password
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@aol.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': '',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertDictContainsSubset(
            {'length': 'Password should be between 6 and 12 characters'},
            message['data'])

    def test_register_user_with_missing_keys(self):
        """
        Test registering a user with missing email
        """
        user = {
            'user_name': 'bison',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': '',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

    def test_register_user_with_blank_firstname(self):
        """
        Test registering a user with a blank first name
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@aol.com',
            'date_registered': '2019-01-01',
            'first_name': '',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': '',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)

    def test_register_with_long_password(self):
        """
        Test registering a user with password longer than 12 characters
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@aol.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123456',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertDictContainsSubset(
            {'length': 'Password should be between 6 and 12 characters'},
            message['data'])

    def test_login(self):
        """
        Test registering a user without a password
        """
        user = {
            'email': 'bisonlou@gmail.com',
            'password': 'Pa$$word123'
        }

        response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 200)

    def test_login_with_missing_data(self):
        """
        Test loging in withou specifying a password
        """
        user = {
            'email': 'bisonlou@gmail.com'
        }

        response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_email(self):
        """
        Test login without email
        """
        user = {
            'email': '',
            'password': 'Pa$$word123'
        }

        response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 400)

    def test_login_with_empty_password(self):
        """
        Test login with empty password
        """
        user = {
            'email': 'bisonlou@gmail.com',
            'password': ''
        }

        response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 400)

    def test_login_with_wrong_password(self):
        """
        Test login with wrong password
        """
        user = {
            'email': 'bisonlou@gmail.com',
            'password': 'Password123'
        }

        response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user))

        self.assertEqual(response.status_code, 401)

    def test_login_with_wrong_email(self):
        """
        Test login with wrongemail
        """
        user = {
            'email': 'bisonlou@outlook.com',
            'password': 'Pa$$word123'
        }

        response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user))

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_get_all_users(self):
        """
        Test getting all users
        """

        user = {
            'email': 'bisonlou@gmail.com',
            'password': 'Pa$$word123'
        }

        login_response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user))

        token = json.loads(login_response.data)

        response = self.test_client.get(
            '/api/v1/users',
            headers={'Authorization': 'Bearer ' +
                     token['access_token']},
            content_type='application/json'
            )

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(message['data'][0]['id'], self.user_id)

    def test_get_all_users_as_non_administrator(self):
        """
        Test getting all users when not an administrator
        Non admins should not be able to see other users but themselves
        """
        user = {
            'user_name': 'bison',
            'email': 'bisonlou@aol.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': ''
        }

        response = self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user))

        login_data = {
            'email': 'bisonlou@aol.com',
            'password': 'Pa$$word123'
        }

        login_response = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(login_data))

        token = json.loads(login_response.data)

        response = self.test_client.get(
            '/api/v1/users',
            headers={'Authorization': 'Bearer ' +
                     token['access_token']},
            content_type='application/json'
            )

        message = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
