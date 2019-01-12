from api import app, jwt
from api.controllers.incident_controller import IncidentController
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)


intervention_controller = IncidentController()
incident_type = 'intervention'


@app.route('/api/v1/interventions', methods=['POST'])
@jwt_required
def add_intervention():
    data = request.get_json()
    user_id = get_jwt_identity()
    kwags = dict(data=data, user_id=user_id, incident_type=incident_type)

    return intervention_controller.create_incident(**kwags)


@app.route('/api/v1/interventions', methods=['GET'])
@jwt_required
def get_interventions():
    user_id = get_jwt_identity()
    kwags = dict(user_id=user_id, incident_type=incident_type)

    return intervention_controller.get_all_incidents(**kwags)


@app.route('/api/v1/interventions/<int:incident_id>', methods=['GET'])
@jwt_required
def get_intervention(incident_id):
    user_id = get_jwt_identity()
    kwags = dict(incident_id=incident_id,
                 user_id=user_id, incident_type=incident_type)

    return intervention_controller.get_incident(**kwags)


@app.route('/api/v1/interventions/<int:incident_id>', methods=['PUT'])
@jwt_required
def alter_intervention(incident_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    kwags = dict(data=data, user_id=user_id,
                 incident_type=incident_type, incident_id=incident_id)

    return intervention_controller.put_incident(**kwags)


@app.route('/api/v1/interventions/<int:incident_id>/<string:query>',
           methods=['PATCH'])
@jwt_required
def update_intervention_location(incident_id, query):
    data = request.get_json()
    user_id = get_jwt_identity()
    kwags = dict(data=data, user_id=user_id,
                 incident_type=incident_type, incident_id=incident_id,
                 query=query)

    return intervention_controller.patch_incident(**kwags)


@app.route('/api/v1/interventions/<int:incident_id>', methods=['DELETE'])
@jwt_required
def delete_intervention(incident_id):
    user_id = get_jwt_identity()
    kwags = dict(user_id=user_id, incident_type=incident_type,
                 incident_id=incident_id)

    return intervention_controller.delete_incident(**kwags)
