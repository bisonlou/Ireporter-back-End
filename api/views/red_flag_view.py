from api import app, jwt
from api.controllers.incident_controller import IncidentController
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)


incident_controller = IncidentController()
incident_type = 'red-flag'


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'greeting': 'Welcome to iReporter',
        'post incident': '/api/v1/redflags',
        'get incidents': '/api/v1/redflags',
        'get incident': '/api/v1/redflags/flag_id',
        'alter incident': '/api/v1/redflags/flag_id',
        'update incident': '/api/v1/redflags/flag_id/key',
        'delete incident': '/api/v1/redflags/flag_id'
    }), 200


@app.route('/api/v1/redflags', methods=['POST'])
@jwt_required
def add_red_flag():

    return incident_controller.create_incident(incident_type)


@app.route('/api/v1/redflags', methods=['GET'])
@jwt_required
def get_red_flags():

    return incident_controller.get_incidents(incident_type)


@app.route('/api/v1/redflags/<int:incident_id>', methods=['GET'])
@jwt_required
def get_red_flag(incident_id):

    return incident_controller.get_incident(incident_type, incident_id)


@app.route('/api/v1/redflags/<int:incident_id>', methods=['PUT'])
@jwt_required
def alter_red_flag(incident_id):

    return incident_controller.put_incident(incident_type, incident_id)


@app.route('/api/v1/redflags/<int:incident_id>/location',
           methods=['PATCH'])
@jwt_required
def update_red_flag_location(incident_id):

    return incident_controller.patch_incident(incident_type, incident_id,
                                                  'location')


@app.route('/api/v1/redflags/<int:incident_id>/comment',
           methods=['PATCH'])
@jwt_required
def update_red_flag_comment(incident_id):

    return incident_controller.patch_incident(incident_type, incident_id,
                                                  'comment')


@app.route('/api/v1/redflags/<int:incident_id>', methods=['DELETE'])
@jwt_required
def delete_red_flag(incident_id):

    return incident_controller.delete_incident(incident_type, incident_id)



@app.route('/api/v1/redflags/<int:incident_id>/escalate', methods=['PATCH'])
@jwt_required
def escalate_red_flag(incident_id):

    return incident_controller.escalate_incident(incident_type,
                                                     incident_id)

