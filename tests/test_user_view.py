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

    def tearDown(self):
        """
        teardown test client
        """
        self.user_services.remove_all()

    def test_register_user(self):
            """
            Test registering a user
            """
            user = {
                'username': 'bisonlou@aol.com',
                'phone': '0753669897',
                'password': 'Password@123'
            }

            response = self.test_client.post(
                '/api/v1/register',
                content_type='application/json',
                data=json.dumps(user))

            message = json.loads(response.data)

            self.assertEqual(message['status'], 201)
            self.assertEqual(self.user_services.count(), 1)
            self.assertEqual(message['data'][0]['message'],
                            'User created')
            self.assertEqual(response.status_code, 201)
