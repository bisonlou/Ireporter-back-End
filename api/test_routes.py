import unittest
import json
from api.routes import app
from api.models import RedFlags


class TestRoutes(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = app.test_client()

        red_flag_1 = {
            'date': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234},
                       {'id': 2, 'name': 'photo_0094.jpg', 'size': 200}
                       ],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Pending',
            'user_id': 1
        }

        red_flag_2 = {
            'date': '2018-12-12',
            'title': 'Magistrate',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Resolved',
            'user_id': 2
        }

        self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag_1)
        )

        self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag_2)
        )

    def tearDown(self):
        """
        teardown test client
        """
        RedFlags.remove_all()

    def test_add_proper_red_flag(self):
        """
        Test adding a red flag with expected details
        """
        red_flag = {
            'date': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': [{'id': 1, 'name': 'photo_0912.jpg', 'size': 134}],
            'videos': [{'id': 1, 'name': 'video_0102.mov', 'size': 2220}],
            'status': 'Pending',
            'user_id': 1
        }

        response = self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 201)
        self.assertEqual(message['data'][0]['message'],
                         'Created red-flag record')
        self.assertEqual(RedFlags.count(), 3)
        self.assertEqual(response.status_code, 201)

    def test_add_bad_red_flag(self):
        """
        Test adding a red flag without expected details
        """
        red_flag = {
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': 'photo_0979.jpg',
            'videos': 'mov_0987.mp4',
            'status': 'Resolved',
        }

        response = self.test_client.post(
            '/api/v1/redflag',
            content_type='application/json',
            data=json.dumps(red_flag)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)
        self.assertEqual(message['error'], 'Bad Request')
        self.assertEqual(RedFlags.count(), 2)
        self.assertEqual(response.status_code, 400)

    def test_get_all_red_flags(self):
        """
        Test getting all red flags
        """
        response = self.test_client.get('/api/v1/redflags')
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEquals(RedFlags().count(), 2)
        self.assertEqual(response.status_code, 200)

    def test_get_existing_red_flag(self):
        """
        Test getting one red flag that exists
        """
        response = self.test_client.get('/api/v1/redflag/1')
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data']['flag_id'], 1)
        self.assertEqual(message['data']['title'], 'Police Officer')
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_red_flag(self):
        """
        Test getting one red flag that does not exist
        """
        response = self.test_client.get('/api/v1/redflag/10')
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(message['error'], 'Not Found')
        self.assertEqual(response.status_code, 404)

    def test_put_red_flag(self):
        """
        Test updating a red flag
        """
        red_flag = {
            "title": "Bribery",
            "comment": "Police officer at CPS Badge #123",
            "date": "2018-01-01",
            "location": "(0.00000,0.00000)",
            "images": [{"id": 1, "name": "photo_0979.jpg", "size": 234}],
            "videos": [{"id": 1, "name": "video_0002.mov", "size": 2340}],
            'status': 'Resolved',
            "user_id": 1
        }

        response = self.test_client.put(
            '/api/v1/redflag/1',
            content_type='application/json',
            data=json.dumps(red_flag)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data'][0]['flag_id'], 1)
        self.assertEqual(message['data'][0]['date'], '2018-01-01')
        self.assertEqual(RedFlags.count(), 2)
        self.assertEqual(response.status_code, 200)

    def test_put_red_flag_with_bad_id(self):
        """
        Test updating a red flag without specifying a flag id
        """
        red_flag = {
            'comment': 'Police officer at CPS Badge #123',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Resolved',
            'user_id': 1
        }

        response = self.test_client.put(
            '/api/v1/redflag/1',
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)
        self.assertEqual(message['error'], 'Bad Request')
        self.assertEqual(response.status_code, 400)

    def test_put_nonexistent_red_flag(self):
        """
        Test updating a red flag which does not exist
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Resolved',
            'user_id': 1
        }

        response = self.test_client.put(
            '/api/v1/redflag/10',
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(message['error'], 'Not Found')
        self.assertEqual(response.status_code, 404)

    def test_put_escalated_red_flag(self):
        """
        Test updating a red flag which has already been resolved
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under Investigation',
            'user_id': 2
        }

        response = self.test_client.put(
            '/api/v1/redflag/2',
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)
        self.assertEqual(message['error'], 'Forbidden')
        self.assertEqual(response.status_code, 403)

    def test_put_red_flag_when_not_owner(self):
        """
        Test updating a red flag which does not belong to the user
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Resolved',
            'user_id': 2
        }

        response = self.test_client.put(
            '/api/v1/redflag/1',
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 401)
        self.assertEqual(message['error'], 'Unauthorised')
        self.assertEqual(response.status_code, 401)

    def test_put_red_flag_without_optional_keys(self):
        """
        Test updating a red flag without optional keys
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'date': '2018-01-01',
            'location': '(0.00000, 0.0000)',
            'status': 'Pending',
            'user_id': 1
        }

        response = self.test_client.put(
            '/api/v1/redflag/1',
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data'][0]['date'], '2018-01-01')
        self.assertEqual(response.status_code, 200)

    def test_update_red_flags_location(self):
        """
        Test updating a redflags location
        """
        red_flag = {
            'comment': 'Police officer at CPS Badge #123',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'title': 'Police Officer #123',
            'videos':  [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Pending',
            'user_id': 1
        }

        response = self.test_client.patch(
            '/api/v1/redflag/1/location',
            content_type='application/json',
            data=json.dumps(red_flag))
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(RedFlags.count(), 2)
        self.assertEqual(
            (message['data'][0]['message']),
            'Updated red-flag record’s location')
        self.assertEquals(RedFlags.get_red_flag(1)[0].location,
                          '(0.00000, 0.0000)')
        self.assertEqual(response.status_code, 200)

    def test_update_red_flags_comment(self):
        """
        Test updating a redflag's comment
        """
        red_flag_update = {
            'comment': 'Took a bribe',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'title': 'Police Officer #123',
            'videos': [{'id': 1, 'name': 'video_0979.jpg', 'size': 234}],
            'status': 'Pending',
            'user_id': 1
        }
        response = self.test_client.patch(
            '/api/v1/redflag/1/comment',
            content_type='application/json',
            data=json.dumps(red_flag_update))
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(RedFlags.count(), 2)
        self.assertEqual(
            (message['data'][0]['message']),
            'Updated red-flag record’s comment')
        self.assertEquals(RedFlags.get_red_flag(1)[0].comment, 'Took a bribe')
        self.assertEqual(response.status_code, 200)

    def test_delete_red_flag(self):
        """
        Test deleting a red flag
        """
        red_flag = {
            'comment': 'Took a bribe',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'title': 'Police Officer #123',
            'videos': [{'id': 1, 'name': 'video_0979.jpg', 'size': 234}],
            'status': 'Pending',
            'user_id': 1
        }

        response = self.test_client.delete(
            '/api/v1/redflag/1',
            content_type='application/json',
            data=json.dumps(red_flag))
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(RedFlags.count(), 1)
        self.assertEqual(
            (message['data'][0]['message']),
            'red-flag record has been deleted')
        self.assertEqual((message['data'][0]['id']), 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existent_red_flag(self):
        """
        Test deleting a red flag
        """
        red_flag = {
            'comment': 'Took a bribe',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'title': 'Police Officer #123',
            'videos': [{'id': 1, 'name': 'video_0979.jpg', 'size': 234}],
            'status': 'Pending',
            'user_id': 1
        }
        response = self.test_client.delete(
            '/api/v1/redflag/10',
            content_type='application/json',
            data=json.dumps(red_flag))
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(RedFlags.count(), 2)
        self.assertEqual(message['error'], 'Not Found')
        self.assertEqual(response.status_code, 404)

    def test_delete_with_bad_id(self):
        """
        Test deleting a red flag
        """
        response = self.test_client.delete('/api/v1/redflag/')
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(RedFlags.count(), 2)
        self.assertEqual(message['error'], 'Not Found')
        self.assertEqual(response.status_code, 404)

    def test_index(self):
        """
        Test default route
        """
        response = self.test_client.get('/')
        message = json.loads(response.data)

        self.assertEqual(message['greeting'], 'Welcome to iReporter')
        self.assertEqual(response.status_code, 200)

