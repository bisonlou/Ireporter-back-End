import unittest
import json
from api.routes import app, red_flags


class TestRoutes(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = app.test_client()

    def tearDown(self):
        """
        teardown test client
        """
        red_flags.clear()    
    
    def post_red_flags(self):
        """
        Function to post sample red flags to list
        """
        red_flag1 = {
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }

        red_flag2 = {
            'date': '2018-12-12',
            'offender': 'Magistrate',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }

        self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag1)
        )

        self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag2)
        )
        
    def test_add_red_flag(self):
        """
        Test adding a red flag with expected details
        """
        red_flag = {
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
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
        self.assertTrue(len(red_flags) == 1)

    def test_get_all_red_flags(self):
        """
        Test getting all red flags
        """
        self.post_red_flags()
        response = self.test_client.get(
            '/api/v1/redflags')
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertTrue(len(red_flags) == 2)    

    def test_get_red_flag(self):
        """
        Test getting all red flags
        """
        
        self.post_red_flags()
        response = self.test_client.get(
            '/api/v1/redflag/1')

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data'][0]['id'], 1)
        self.assertEqual(message['data'][0]['offender'], 'Police Officer')   
        self.assertEqual(len(message['data']), 1)

    def test_alter_entire_red_flag(self):
        """
        Test getting all red flags
        """
        self.post_red_flags()

        red_flag_2 = {            
            "comment": "Police officer at CPS Badge #123",
            "date": "2018-01-01",
            "image": "photo_0001.jpg",
            "location": "(0.00000, 0.0000)",
            "offender": "Police Officer #123",
            "video": "mov_00001.mp4"
        }

        response = self.test_client.put(
            '/api/v1/redflag/1',
            content_type='application/json',
            data=json.dumps(red_flag_2)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data'][0]['id'], 1)   
        self.assertEqual(message['data'][0]['offender'], 'Police Officer #123')   
        self.assertEqual(message['data'][0]['date'], '2018-01-01')   
        self.assertEqual(message['data'][0]['image'], 'photo_0001.jpg')   
        self.assertEqual(message['data'][0]['location'], '(0.00000, 0.0000)')   
        self.assertEqual(message['data'][0]['video'], 'mov_00001.mp4')   
        self.assertEqual(message['data'][0]['comment'], 'Police officer at CPS Badge #123')   
        self.assertEqual(len(message['data']), 1)
        self.assertEqual(len(red_flags), 2)

    def test_update_red_flags_location(self):
        """
        Test updating a redflags location
        """
        self.post_red_flags()

        response = self.test_client.patch(
            '/api/v1/redflag/1/(0.000000, 0.000000)')

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertTrue(len(red_flags) == 2)
        self.assertEqual(
            (message['data'][0]['message']),
            'Updated red-flag record’s location')
        self.assertEqual((message['data'][0]['id']), 1)
        self.assertEquals(red_flags[0]['location'], '(0.000000, 0.000000)')

    def test_update_red_flags_comment(self):
        """
        Test updateing a redflags comment
        """
        self.post_red_flags()
        response = self.test_client.patch(
            "/api/v1/redflag/1/'Took a bribe'")

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertTrue(len(red_flags) == 2)
        self.assertEqual(
            (message['data'][0]['message']),
            'Updated red-flag record’s comment')
        self.assertEqual((message['data'][0]['id']), 1)
        self.assertEquals(red_flags[0]['comment'], 'Took a bribe')

    def test_delete_red_flag(self):
        """
        Test deleting a red flag
        """
        self.post_red_flags()

        response = self.test_client.delete('/api/v1/redflag/1')
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertTrue(len(red_flags) == 1)
        self.assertEqual(
            (message['data'][0]['message']),
            'red-flag record has been deleted')
        self.assertEqual((message['data'][0]['id']), 1)

        response = self.test_client.delete('/api/v1/redflag/2')
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertTrue(len(red_flags) == 0)
        self.assertEqual(
            (message['data'][0]['message']),
            'red-flag record has been deleted')
        self.assertEqual((message['data'][0]['id']), 2)