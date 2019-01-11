from api.validators.Incident_Validator import ValidateIncident
from api.models.incident_model import Incident, IncidentServices
from api.models.user_model import User, UserServices
from flask import Flask, request, json, jsonify, abort
from api import app

incident_validator = ValidateIncident()
incident_services = IncidentServices()
user_services = UserServices()


class IncidentController():

    def create_incident(self, data, user_id, incident_type):
        data['createdBy'] = user_id
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

    def get_incident(self, incident_id, user_id, incident_type):
        try:
            incident = incident_services.get_incident(
                                    incident_id, incident_type)

            if not incident_validator.is_owner(incident, user_id):
                abort(403)

            return jsonify({'status': 200, 'data': incident.to_dict()}), 200

        except ValueError:
            abort(404)

    def get_all_incidents(self, user_id, incident_type):
        user = user_services.get_user_by_id(user_id)
        is_admin = user.is_admin

        incidents = incident_services.get_all(user_id, is_admin, incident_type)
        return jsonify({'status': 200, 'data': incidents})

    def put_incident(self, data, incident_id, incident_type, user_id):
        data['createdBy'] = user_id
        data['id'] = incident_id

        if not incident_validator.has_required_keys(data):
            abort(400)      

        update_incident = Incident(**data)

        try:
            existing_incident = incident_services.get_incident(
                                incident_id, incident_type)

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

        except ValueError:
            abort(404)

    def patch_incident(self, data, incident_id,
                       update_key, incident_type, user_id):
        data['createdBy'] = user_id

        if not incident_validator.has_required_keys(data):
            abort(400)

        try:
            existing_incident = incident_services.get_incident(
                         incident_id, incident_type)

            if not incident_validator.is_owner(existing_incident, user_id):
                abort(401)
            if not incident_validator.is_modifiable(existing_incident):
                abort(403)

            data['id'] = incident_id
            update_incident = Incident(**data)

            incident_services.patch_incident(existing_incident,
                                             update_incident, update_key)
            success_response = {
                'id': incident_id,
                'message': f'Updated {incident_type} record’s {update_key}'
            }

            return jsonify({'status': 200, 'data': success_response}), 200

        except ValueError:
            abort(404)

    def delete_incident(self, incident_id, user_id, incident_type):
        try:

            existing_incident = incident_services.get_incident(
                         incident_id, incident_type)
            if not incident_validator.is_owner(existing_incident, user_id):
                abort(401)
            if not incident_validator.is_modifiable(existing_incident):
                abort(403)

            incident_services.delete_incident(existing_incident,
                                              incident_type)
            success_response = {
                'id': incident_id,
                'message': f'{incident_type} record has been deleted'}
            return jsonify({'status': 200, 'data': success_response}), 200

        except ValueError:
            abort(404)

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
