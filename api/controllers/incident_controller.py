from api.validators.Incident_Validator import ValidateIncident
from api.models.incident_model import Incident, IncidentServices
from api.models.user_model import User, UserServices
from flask import Flask, request, json, jsonify, abort
from api import app

incident_validator = ValidateIncident()
incident_services = IncidentServices()
user_services = UserServices()


class IncidentController():

    def create_incident(self, **kwags):
        data = kwags['data']
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']

        data['created_by'] = user_id
        data['status'] = 'Pending'

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
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']

        user = user_services.get_user_by_id(user_id)
        is_admin = user.is_admin

        incidents = incident_services.get_all(user_id, is_admin, incident_type)
        return jsonify({'status': 200, 'data': incidents})

    def put_incident(self, **kwags):
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
            abort(401)

        if not incident_validator.is_modifiable(existing_incident):
            abort(403)

        incident_services.put_incident(
            existing_incident, update_incident, incident_type)

        updated_incident = incident_services.get_incident(
                            incident_id, incident_type)

        return jsonify({'status': 200, 'data':
                        updated_incident.to_dict()})

    def patch_incident(self, **kwags):
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
            abort(401)
        if not incident_validator.is_modifiable(existing_incident):
            abort(403)

        update_incident = Incident(**data)

        incident_services.patch_incident(existing_incident,
                                         update_incident, update_key)
        success_response = {
            'id': incident_id,
            'message': f'Updated {incident_type} record’s {update_key}'
        }

        return jsonify({'status': 200, 'data': success_response}), 200

    def delete_incident(self, **kwags):
        user_id = kwags['user_id']
        incident_type = kwags['incident_type']
        incident_id = kwags['incident_id']

        existing_incident = incident_services.get_incident(
                            incident_id, incident_type)
        if not existing_incident:
            abort(404)

        if not incident_validator.is_owner(existing_incident, user_id):
            abort(401)
        if not incident_validator.is_modifiable(existing_incident):
            abort(403)

        incident_services.delete_incident(existing_incident, incident_type)
        success_response = {
            'id': incident_id,
            'message': f'{incident_type} record has been deleted'}

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
