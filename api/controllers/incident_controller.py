from api.validators.Incident_Validator import ValidateIncident
from api.models.incident_model import Incident, IncidentServices
from api.models.user_model import User, UserServices
from flask import Flask, request, json, jsonify, abort
from api import app

incident_validator = ValidateIncident()
incident_services = IncidentServices()
user_services = UserServices()


class IncidentController():
    '''

    Class to handle incident related routes

    '''

    def create_incident(self, **kwags):
        '''
        Function to create an incident
        Validates the incident data
        If data passes validation an incident is created

        '''
        data = kwags['data']
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']

        data['created_by'] = user_id
        data['status'] = 0

        if not incident_validator.has_required_keys(data):
            abort(400)

        incident_id = incident_services.get_next_id(incident_type)

        data['id'] = incident_id
        new_incident = Incident(**data)

        incident_services.create_incident(new_incident, incident_type)

        success_response = {'id': incident_id, 'message':
                            f'Created {incident_type} record'}
        return jsonify({'status': 201, 'data': [success_response]}), 201

    def get_incident(self, **kwags):
        '''
        Function to retun an incident give an incident id
        Validates the incident exists and belongs to this user
        If validation is passed an incident is returned

        '''
        incident_id = kwags['incident_id']
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']

        incident = incident_services.get_incident(
                                incident_id, incident_type)
        if not incident:
            abort(404)

        if not incident_validator.is_owner(incident, user_id):
            abort(403)

        return jsonify({'status': 200, 'data': incident.to_dict()}), 200

    def get_all_incidents(self, **kwags):
        '''
        Function to retun all incident given an incident id

        '''
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']

        user = user_services.get_user_by_id(user_id)

        incidents = incident_services.get_all(user_id, user.is_admin,
                                              incident_type)

        return jsonify({'status': 200, 'data': incidents})

    def put_incident(self, **kwags):
        '''
        Function to update an entire incident
        Validates the incident exists and belongs to this user
        If validation is passed the incident is updated
        and the updted incident is returned

        '''
        data = kwags['data']
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']
        incident_id = kwags['incident_id']

        data['created_by'] = user_id
        data['id'] = incident_id

        if not incident_validator.has_required_keys(data):
            abort(400)

        update_incident = Incident(**data)

        existing_incident = incident_services.get_incident(
                                incident_id, incident_type)
        if not existing_incident:
            abort(404)

        if not incident_validator.is_owner(existing_incident, user_id):
            abort(403)

        if not incident_validator.is_modifiable(existing_incident):
            abort(403)

        incident_services.put_incident(
            existing_incident, update_incident, incident_type)

        updated_incident = incident_services.get_incident(
                            incident_id, incident_type)

        return jsonify({'status': 200, 'data':
                        updated_incident.to_dict()})

    def patch_incident(self, **kwags):
        '''
        Function to update a property of an incident
        Validates the incident exists and belongs to this user
        If validation is passed the incidentpropert is updated
        and a success message is returned

        '''
        data = kwags['data']
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']
        incident_id = kwags['incident_id']
        update_key = kwags['query']

        data['created_by'] = user_id
        data['id'] = incident_id

        if not incident_validator.has_required_keys(data):
            abort(400)

        existing_incident = incident_services.get_incident(
                            incident_id, incident_type)
        if not existing_incident:
            abort(404)

        if not incident_validator.is_owner(existing_incident, user_id):
            abort(403)

        if not incident_validator.is_modifiable(existing_incident):
            abort(403)

        data['status'] = existing_incident.status
        update_incident = Incident(**data)

        incident_services.patch_incident(existing_incident,
                                         update_incident, update_key)
        success_response = {
            'id': incident_id,
            'message': f'Updated {incident_type} record’s {update_key}'
        }

        return jsonify({'status': 200, 'data': success_response}), 200

    def delete_incident(self, **kwags):
        '''
        Function to delete an incident
        Validates the incident exists and belongs to this user
        or the user is an admin
        If validation is passed the incident is deleted
        and a success message is returned

        '''
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']
        incident_id = kwags['incident_id']

        user = user_services.get_user_by_id(user_id)
        if not user:
            abort(401)

        existing_incident = incident_services.get_incident(
                            incident_id, incident_type)
        if not existing_incident:
            abort(404)

        if not incident_validator.is_owner(existing_incident, user_id):
            abort(403)

        if not user.is_admin:
            if not incident_validator.is_modifiable(existing_incident):
                abort(403)

        incident_services.delete_incident(existing_incident, incident_type)
        success_response = {
            'id': incident_id,
            'message': f'{incident_type} record has been deleted'}

        return jsonify({'status': 200, 'data': success_response}), 200

    def escalate_incident(self, **kwags):
        '''
        Function to change the status of an incident
        Validates the incident exists and the user is an admin
        If validation is passed the incident is escalated
        and a success message is returned

        '''
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']
        incident_id = kwags['incident_id']

        user = user_services.get_user_by_id(user_id)
        if not user:
            abort(401)

        if not user.is_admin:
            abort(403)

        existing_incident = incident_services.get_incident(
                            incident_id, incident_type)
        if not existing_incident:
            abort(404)

        incident_services.escalate_incident(existing_incident)
        success_response = {
            'id': incident_id,
            'message': f'{incident_type} record has been escalated'}

        return jsonify({'status': 200, 'data': success_response}), 200


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'status': 400, 'error': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorised(error):
        return jsonify({'status': 401, 'error': 'Unauthorised'}), 401

    @app.errorhandler(403)
    def forbiden(error):
        return jsonify({'status': 403, 'error': 'Forbidden'}), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 404, 'error': 'Not Found'}), 404
