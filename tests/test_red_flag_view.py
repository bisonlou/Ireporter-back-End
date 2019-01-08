import unittest
import json
from api import app, test_client
from api.models.incident_model import IncidentServices
from api.models.user_model import UserServices


class TestRedFlagView(unittest.TestCase):

    def setUp(self):
        """
        Setup test client
        """
        self.test_client = test_client
        self.incident_services = IncidentServices()
        self.user_services = UserServices()

        user_1 = {
            'username': 'bisonlou@gmail.com',
            'password': 'Password@123',
            'phone': '256753669897'
        }

        user_2 = {
            'username': 'bisonlou@aol.com',
            'password': 'Password@123',
            'phone': '256753669897'
        }

        self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user_1)
        )

        self.test_client.post(
            '/api/v1/register',
            content_type='application/json',
            data=json.dumps(user_2)
        )

        response_1 = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user_1)
        )

        response_2 = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user_2)
        )

        self.token = json.loads(response_1.data)
        self.token_2 = json.loads(response_2.data)

        red_flag_1 = {
            'date': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234},
                       {'id': 2, 'name': 'photo_0094.jpg', 'size': 200}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        red_flag_2 = {
            'date': '2018-12-12',
            'title': 'Magistrate',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_1)
        )

        self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.token_2['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_2)
        )

    def tearDown(self):
        """
        teardown test client
        """
        self.incident_services.remove_all('red-flag')
        self.user_services.remove_all()

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
            'videos': [{'id': 1, 'name': 'video_0102.mov', 'size': 2220}]
        }

        response = self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )

        message = json.loads(response.data)
        self.assertEqual(message['status'], 201)
        self.assertEqual(message['data'][0]['message'],
                         'Created red-flag record')
        self.assertEqual(self.incident_services.count('red-flag'), 3)
        self.assertEqual(response.status_code, 201)

    def test_add_bad_red_flag(self):
        """
        Test adding a red flag without expected details
        """
        red_flag = {
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': 'photo_0979.jpg',
            'videos': 'mov_0987.mp4'
        }

        response = self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)
        self.assertEqual(message['error'], 'Bad Request')
        self.assertEqual(self.incident_services.count('red-flag'), 2)
        self.assertEqual(response.status_code, 400)

    def test_get_all_red_flags(self):
        """
        Test getting all red flags
        """
        response = self.test_client.get(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' + self.token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEquals(self.incident_services.count('red-flag'), 2)
        self.assertEquals(len(message['data']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_existing_red_flag(self):
        """
        Test getting one red flag that exists
        """
        response = self.test_client.get(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' + self.token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data']['id'], 1)
        self.assertEqual(message['data']['title'], 'Police Officer')
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_red_flag(self):
        """
        Test getting one red flag that does not exist
        """
        response = self.test_client.get(
            '/api/v1/redflags/3',
            headers={'Authorization': 'Bearer ' + self.token['access_token']})
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
            "status": "Under investigation"
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data']['id'], 1)
        self.assertEqual(message['data']['date'], '2018-01-01')
        self.assertEqual(self.incident_services.count('red-flag'), 2)
        self.assertEqual(response.status_code, 200)

    def test_put_red_flag_with_bad_id(self):
        """
        Test updating a red flag without specifying a title
        """
        red_flag = {
            'comment': 'Police officer at CPS Badge #123',
            'date': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
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
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/redflags/10',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
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
            'date': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234},
                       {'id': 2, 'name': 'photo_0094.jpg', 'size': 200}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Under investigation'
        }
        # change the status of red flag 1
        self.test_client.patch(
            '/api/v1/redflags/1/status',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )

        # try updating a red flag whose status is now 'under investigation'
        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
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
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.token_2['access_token']},
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
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' + self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data']['date'], '2018-01-01')
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
            'status': 'Under investigation'
        }

        response = self.test_client.patch(
            '/api/v1/redflags/1/location',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag))
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(
            (message['data']['message']),
            'Updated red-flag record’s location')
        self.assertEquals(self.incident_services.
                          get_incident(1, 'red-flag').location,
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
            'status': 'Under investigation'
        }
        response = self.test_client.patch(
            '/api/v1/redflags/1/comment',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_update))

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(
            (message['data']['message']),
            'Updated red-flag record’s comment')
        self.assertEquals(self.incident_services.
                          get_incident(1, 'red-flag').comment,
                          'Took a bribe')
        self.assertEqual(response.status_code, 200)

    def test_delete_red_flag(self):
        """
        Test deleting a red flag
        """
        response = self.test_client.delete(
                    '/api/v1/redflags/1',
                    content_type='application/json',
                    headers={'Authorization': 'Bearer ' +
                             self.token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(self.incident_services.count('red-flag'), 1)
        self.assertEqual(
            (message['data']['message']),
            'red-flag record has been deleted')
        self.assertEqual((message['data']['id']), 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existent_red_flag(self):
        """
        Test deleting a red flag
        """

        response = self.test_client.delete(
            '/api/v1/redflags/10',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' +
                     self.token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(self.incident_services.count('red-flag'), 2)
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

    