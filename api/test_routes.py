import unittest
import json
import models
from run import app


class TestRoutes(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = app.test_client()

    def test_add_red_flag(self):
        """
        Test adding a red flag with expected details
        """
        red_flag = {
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'description': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }

        response = self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag)
        )

        message = json.loads(response.data)
        print(message['data'][0]['message'])
        self.assertEqual(message['status'], 201)  
        self.assertEqual(message['data'][0]['message'], 'Created red-flag record')  
        assert(len(models.red_flags) > 0)