import unittest
import json
from api import app, test_client
from api.models.incident_model import IncidentServices
from api.models.user_model import UserServices


class TestInterventionView(unittest.TestCase):

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
                'user_name': 'bisonlou',
                'email': 'bisonlou@gmail.com',
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

        self.admin_token = json.loads(response_1.data)
        self.non_admin_token = json.loads(response_2.data)

        intervention_1 = {
            'created_on': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'intervention',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234},
                       {'id': 2, 'name': 'photo_0094.jpg', 'size': 200}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        intervention_2 = {
            'created_on': '2018-12-12',
            'title': 'Magistrate',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'intervention',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}]
        }

        self.test_client.post(
            '/api/v1/interventions',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention_1)
        )

        self.test_client.post(
            '/api/v1/interventions',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention_2)
        )

    def tearDown(self):
        """
        teardown test client
        """
        self.incident_services.remove_all('intervention')
        self.user_services.remove_all()

    def test_add_proper_intervention(self):
        """
        Test adding a intervention with expected details
        """
        intervention = {
            'created_on': '2018-12-24',
            'title': 'Police Officer',
            'comment': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'type': 'intervention',
            'images': [{'id': 1, 'name': 'photo_0912.jpg', 'size': 134}],
            'videos': [{'id': 1, 'name': 'video_0102.mov', 'size': 2220}]
        }

        response = self.test_client.post(
            '/api/v1/interventions',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
        )

        message = json.loads(response.data)
        self.assertEqual(message['status'], 201)
        self.assertEqual(message['data'][0]['message'],
                         'Created intervention record')
        self.assertEqual(self.incident_services.count('intervention'), 3)
        self.assertEqual(response.status_code, 201)

    def test_add_bad_intervention(self):
        """
        Test adding a intervention with
        some key values not strings
        """
        intervention = {
            'created_on': '2018-12-12',
            'title': 162,
            'comment': 'Took a bribe',
            'location': '(-65.712557, -15.000182)',
            'type': 'intervention',
            'images': 'photo_0979.jpg',
            'videos': 'mov_0987.mp4'
        }

        response = self.test_client.post(
            '/api/v1/interventions',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)
        self.assertEqual(message['error'], 'Bad Request')
        self.assertEqual(self.incident_services.count('intervention'), 2)
        self.assertEqual(response.status_code, 400)

    def test_get_all_interventions_as_admin(self):
        """
        Test getting all interventions when user is admin
        """
        response = self.test_client.get(
            '/api/v1/interventions',
            headers={'Authorization': 'Bearer ' + self.admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(len(message['data']), 2)
        self.assertEqual(response.status_code, 200)

    def test_get_all_interventions_as_non_admin(self):
        """
        Test getting all interventions when user is not admin
        """
        response = self.test_client.get(
            '/api/v1/interventions',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(len(message['data']), 1)
        self.assertEqual(response.status_code, 200)

    def test_get_existing_intervention(self):
        """
        Test getting one intervention that exists
        """
        response = self.test_client.get(
            '/api/v1/interventions/1',
            headers={'Authorization': 'Bearer ' + self.admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data']['id'], 1)
        self.assertEqual(message['data']['title'], 'Police Officer')
        self.assertEqual(response.status_code, 200)

    def test_get_non_existent_intervention(self):
        """
        Test getting one intervention that does not exist
        """
        response = self.test_client.get(
            '/api/v1/interventions/3',
            headers={'Authorization': 'Bearer ' + self.admin_token['access_token']})
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(message['error'], 'Not Found')
        self.assertEqual(response.status_code, 404)

    def test_put_intervention(self):
        """
        Test updating a intervention
        """
        intervention = {
            "title": "Bribery",
            "comment": "Police officer at CPS Badge #123",
            "created_on": "2018-01-01",
            "location": "(0.00000,0.00000)",
            "type": "intervention",
            "images": [{"id": 1, "name": "photo_0979.jpg", "size": 234}],
            "videos": [{"id": 1, "name": "video_0002.mov", "size": 2340}],
            "status": "Under investigation"
        }

        response = self.test_client.put(
            '/api/v1/interventions/1',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
            )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(message['data']['id'], 1)
        self.assertEqual(self.incident_services.count('intervention'), 2)
        self.assertEqual(response.status_code, 200)

    def test_put_intervention_without_title(self):
        """
        Test updating a intervention without specifying a title
        """
        intervention = {
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'intervention',
            'videos': [{'id': 1, 'name': 'video_0002.mov', 'size': 2340}],
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/interventions/1',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 400)
        self.assertEqual(message['error'], 'Bad Request')
        self.assertEqual(response.status_code, 400)

    def test_put_nonexistent_intervention(self):
        """
        Test updating a intervention which does not exist
        """
        intervention = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'intervention',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/interventions/10',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)
        self.assertEqual(message['error'], 'Not Found')
        self.assertEqual(response.status_code, 404)

    def test_put_intervention_when_not_owner(self):
        """
        Test updating a intervention which does not belong to the user
        Expect 403 - Forbiden
        """
        intervention = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'intervention',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Pending'
        }

        response = self.test_client.put(
            '/api/v1/interventions/1',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_put_escalated_intervention(self):
        """
        Test updating an intervention which has already been escalaed
        Expect 403 - Forbiden
        """
        intervention = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'intervention',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Pending'
        }

        self.test_client.patch(
            '/api/v1/interventions/2/escalate',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']}
        )

        response = self.test_client.put(
            '/api/v1/interventions/2',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_put_intervention_without_optional_keys(self):
        """
        Test updating a intervention without optional keys
        """
        intervention = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'location': '(0.00000, 0.0000)',
            'type': 'intervention',
            'status': 'Under investigation'
        }

        response = self.test_client.put(
            '/api/v1/interventions/1',
            headers={'Authorization': 'Bearer ' + self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention)
        )
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(response.status_code, 200)

    def test_update_interventions_location(self):
        """
        Test updating a interventions location
        """
        intervention = {
            'title': 'Bribery',
            'comment': 'Police officer at CPS Badge #123',
            'created_on': '2018-01-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00000, 0.0000)',
            'type': 'intervention',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}],
            'status': 'Under investigation'
        }

        response = self.test_client.patch(
            '/api/v1/interventions/1/location',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention))
        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(
            (message['data']['message']),
            'Updated intervention record’s location')
        self.assertEqual(self.incident_services.
                         get_incident(1, 'intervention').location,
                         '(0.00000, 0.0000)')
        self.assertEqual(response.status_code, 200)

    def test_update_interventions_comment(self):
        """
        Test updating a redflag's comment
        """
        intervention = {
            'title': 'Bribery at kabalagala juction',
            'comment': 'Took a bribe',
            'created_on': '2018-11-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00500, 0.0000)',
            'type': 'intervention',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}]
        }

        response = self.test_client.patch(
            '/api/v1/interventions/1/comment',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention))

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(
            (message['data']['message']),
            'Updated intervention record’s comment')
        self.assertEqual(self.incident_services.
                         get_incident(1, 'intervention').comment,
                         'Took a bribe')
        self.assertEqual(response.status_code, 200)

    def test_update_escalated_interventions(self):
        """
        Test updating a redflag's comment
        """
        intervention = {
            'title': 'Bribery at kabalagala juction',
            'comment': 'Took a bribe',
            'created_on': '2018-11-01',
            'images': [{'id': 1, 'name': 'photo_0979.jpg', 'size': 234}],
            'location': '(0.00500, 0.0000)',
            'type': 'intervention',
            'videos': [{'id': 1, 'name': 'mov_0002.mp4', 'size': 2340}]
        }

        self.test_client.patch(
            '/api/v1/interventions/2/escalate',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']},
            content_type='application/json')

        response = self.test_client.patch(
            '/api/v1/interventions/2/comment',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']},
            content_type='application/json',
            data=json.dumps(intervention))

        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_delete_intervention(self):
        """
        Test deleting a intervention
        """
        response = self.test_client.delete(
                    '/api/v1/interventions/1',
                    content_type='application/json',
                    headers={'Authorization': 'Bearer ' +
                             self.admin_token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 200)
        self.assertEqual(self.incident_services.count('intervention'), 1)
        self.assertEqual(
            (message['data']['message']),
            'intervention record has been deleted')
        self.assertEqual((message['data']['id']), 1)
        self.assertEqual(response.status_code, 200)

    def test_delete_intervention_when_not_owner(self):
        """
        Test deleting an intervention that was not created by the user
        Expect 403
        """

        response = self.test_client.delete(
            '/api/v1/interventions/1',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)

    def test_delete_non_existent_intervention(self):
        """
        Test deleting an intervention that does not exist
        Expect 404
        """

        response = self.test_client.delete(
            '/api/v1/interventions/10',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 404)

    def test_delete_intervention_under_investigation(self):
        """
        Test deleting an intervention that has been escalated
        """
        self.test_client.patch(
            '/api/v1/interventions/2/escalate',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' +
                     self.admin_token['access_token']})

        response = self.test_client.delete(
            '/api/v1/interventions/2',
            content_type='application/json',
            headers={'Authorization': 'Bearer ' +
                     self.non_admin_token['access_token']})

        message = json.loads(response.data)

        self.assertEqual(message['status'], 403)
