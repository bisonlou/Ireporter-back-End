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
            'user_name': 'bison',
            'email': 'bisonlou@aol.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': ''
        }

        user_2 = {
            'user_name': 'bison',
            'email': 'bisonlou@yahoo.com',
            'date_registered': '2019-01-01',
            'first_name': 'bison',
            'last_name': 'lou',
            'phone_number': '0753669897',
            'password': 'Pa$$word123',
            'other_names': ''
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

        user1_login = {
            'email': 'bisonlou@aol.com',
            'password': 'Pa$$word123'
        }

        user2_login = {
            'email': 'bisonlou@yahoo.com',
            'password': 'Pa$$word123'
        }

        response_1 = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user1_login)
        )

        response_2 = self.test_client.post(
            '/api/v1/login',
            content_type='application/json',
            data=json.dumps(user2_login)
        )

        self.admin_token = json.loads(response_1.data)
        self.non_admin_token = json.loads(response_2.data)

        red_flag_1 = {
            'created_on': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234},
                       {'id': 2, 'name': 'photo_0094.jpg', 'size': 200}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        red_flag_2 = {
            'created_on': '2018-12-12',
            'title': 'Magistrate',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_1)
        )

        self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
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
        Test adding a red flag with expected keys
        Expect 201
        """
        red_flag = {
            'created_on': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': [{'id': 1, 'name': 'photo_0912.jpg', 'size': 134}],
            'videos': [{'id': 1, 'name': 'video_0102.mov', 'size': 2220}]
        }

        response = self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
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
        Test adding a red flag with images
        and videos keys not of type list but string
        Expect 400
        """
        red_flag = {
            'created_on': '2018-12-12',
            'title': 'Police officer at CPS Badge #162',
            'comment': 'Took a bribe',
            'location': '(-65.712557, -15.000182)',
            'type': 'red-flag',
            'images': 'photo_0979.jpg',
            'videos': 'mov_0987.mp4'
        }

        response = self.test_client.post(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)
        self.assertEqual(self.incident_services.count('red-flag'), 2)
        self.assertEqual(response.status_code, 400)

    def test_get_all_red_flags_as_admin(self):
        """
        Test getting all red flags as a normal user
        token is by an administrative user
        2 red flag expected
        """
        response = self.test_client.get(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' + self.admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEquals(self.incident_services.count('red-flag'), 2)
        self.assertEqual(len(message['data']), 2)
        self.assertEqual(response.status_code, 200)

    def test_get_all_redflags_as_non_admin(self):
        """
        Test getting all red flags when user is not admin
        """
        response = self.test_client.get(
            '/api/v1/redflags',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(len(message['data']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_existing_red_flag(self):
        """
        Test getting one red flag that exists
        Expect 200
        """
        response = self.test_client.get(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data']['id'], 1)

    def test_get_red_flag_when_not_owner(self):
        """
        Test getting one red flag that does not belong to the user
        Expect 403
        """
        response = self.test_client.get(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_get_non_existent_red_flag(self):
        """
        Test getting one red flag that does not exist
        Expect 404
        """
        response = self.test_client.get(
            '/api/v1/redflags/3',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)

    def test_put_red_flag(self):
        """
        Test updating a red flag
        Expect 200
        """
        red_flag = {
            "title": "Bribery",
            "comment": "Police officer at CPS Badge #123",
            "created_on": "2018-01-01",
            "location": "(0.00000,0.00000)",
            "type": "red-flag",
            "images": [{"id": 1, "name": "photo_0979.jpg", "size": 234}],
            "videos": [{"id": 1, "name": "video_0002.mov", "size": 2340}],
            "status": "Under investigation"
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)

    def test_put_red_flag_without_title(self):
        """
        Test updating a red flag without specifying a title
        Expect 400
        """
        red_flag = {
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
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
        Expect 404
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/redflags/10',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(message['error'], 'Not Found')
        self.assertEqual(response.status_code, 404)

    def test_patch_escalated_red_flag(self):
        """
        Test updating a red flag which has already been escalated
        Expect 403
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}]
        }
        # change the status of red flag 1
        self.test_client.patch(
            '/api/v1/redflags/2/escalate',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json'
        )

        # try updating a red flag whose status is now 'under investigation'
        response = self.test_client.patch(
            '/api/v1/redflags/2/location',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_put_red_flag_when_not_owner(self):
        """
        Test updating a red flag which does not belong to the user
        Expect 403
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Pending'
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_put_red_flag_without_optional_keys(self):
        """
        Test updating a red flag without optional keys
        Expect 200
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/redflags/1',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(response.status_code, 200)

    def test_update_red_flags_location(self):
        """
        Test updating a redflags location
        """
        red_flag = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'status': 'Under investigation'
        }

        response = self.test_client.patch(
            '/api/v1/redflags/1/location',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag))
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(
            (message['data']['message']),
            'Updated red-flag record’s location')
        self.assertEqual(self.incident_services.
                         get_incident(1, 'red-flag').location,
                         '(0.00000, 0.0000)')
        self.assertEqual(response.status_code, 200)

    def test_update_red_flags_comment(self):
        """
        Test updating a redflag's comment
        """
        red_flag_update = {
            'title': 'Bribery',
            'comment': 'Took a bribe',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under investigation'
        }
        response = self.test_client.patch(
            '/api/v1/redflags/1/comment',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_update))

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(
            (message['data']['message']),
            'Updated red-flag record’s comment')
        self.assertEqual(self.incident_services.
                         get_incident(1, 'red-flag').comment,
                         'Took a bribe')        
        self.assertEqual(response.status_code, 200)

    def test_update_red_flags_comment_with_missing_comment(self):
        """
        Test updating a redflag's comment without a comment
        """
        red_flag_update = {
            'title': 'Bribery',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under investigation'
        }
        response = self.test_client.patch(
            '/api/v1/redflags/1/comment',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_update))

        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)

    def test_update_non_existent_flag(self):
        """
        Test updating a redflag's comment when the 
        red flag doest exist
        """
        red_flag_update = {
            'title': 'Bribery',
            'comment': 'Took a bribe',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under investigation'
        }
        response = self.test_client.patch(
            '/api/v1/redflags/10/comment',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_update))

        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)

    def test_update_flag_when_not_owner(self):
        """
        Test updating a redflag's comment when the
        red flag doest belong to the user
        """
        red_flag_update = {
            'title': 'Bribery',
            'comment': 'Took a bribe',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'red-flag',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under investigation'
        }
        response = self.test_client.patch(
            '/api/v1/redflags/1/comment',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(red_flag_update))

        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_delete_red_flag(self):
        """
        Test deleting a red flag
        """
        response = self.test_client.delete(
                    '/api/v1/redflags/1',
                    content_type='application/json',
                    headers={'Authorization': 'Bearer ' +
                             self.admin_token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(self.incident_services.count('red-flag'), 1)
        self.assertEqual(
            (message['data']['message']),
            'red-flag record has been deleted')

    def test_delete_non_existent_red_flag(self):
        """
        Test deleting a red flag that does not exist
        Expect 404
        """

        response = self.test_client.delete(
            '/api/v1/redflags/10',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
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

    def test_escalate_non_existent_flag(self):
        '''
        Test escalating a red flag that does not exixt
        Expect 404
        '''

        response = self.test_client.patch(
                    'api/v1/redflags/10/escalate',
                    headers={'authorization': 'Bearer ' +
                             self.admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)

    def test_escalate_when_user_not_admin(self):
        '''
        Test escalating a red flag when not admin
        Expect 403
        '''

        response = self.test_client.patch(
                    'api/v1/redflags/10/escalate',
                    headers={'authorization': 'Bearer ' +
                             self.non_admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

