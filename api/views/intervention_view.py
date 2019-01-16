from api import app, jwt
from api.controllers.incident_controller import IncidentController
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)


incident_controller = IncidentController()
incident_type = 'intervention'


@app.route('/api/v1/interventions', methods=['POST'])
@jwt_required
def add_intervention():

    return incident_controller.create_incident(incident_type)


@app.route('/api/v1/interventions', methods=['GET'])
@jwt_required
def get_interventions():

    return incident_controller.get_incidents(incident_type)


@app.route('/api/v1/interventions/<int:incident_id>', methods=['GET'])
@jwt_required
def get_intervention(incident_id):    

    return incident_controller.get_incident(incident_type, incident_id)


@app.route('/api/v1/interventions/<int:incident_id>', methods=['PUT'])
@jwt_required
def put_intervention(incident_id):

    return incident_controller.put_incident(incident_type, incident_id)


@app.route('/api/v1/interventions/<int:incident_id>/location',
           methods=['PATCH'])
@jwt_required
def update_intervention_location(incident_id):

    return incident_controller.patch_incident(incident_type, incident_id,
                                                  'location')


@app.route('/api/v1/interventions/<int:incident_id>/comment',
           methods=['PATCH'])
@jwt_required
def update_intervention_comment(incident_id):

    return incident_controller.patch_incident(incident_type, incident_id,
                                                  'comment')


@app.route('/api/v1/interventions/<int:incident_id>', methods=['DELETE'])
@jwt_required
def delete_intervention(incident_id):

    return incident_controller.delete_incident(incident_type, incident_id)


@app.route('/api/v1/interventions/<int:incident_id>/escalate',
           methods=['PATCH'])
@jwt_required
def escalate_intervention(incident_id):

    return incident_controller.escalate_incident(incident_type,
                                                     incident_id)
