from api import app, jwt
from api.controllers.incident_controller import IncidentController
from flask import request, jsonify
from flask_jwt_extended import (jwt_required, get_jwt_identity)


red_flag_controller = IncidentController()
incident_type = 'red-flag'


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'greeting': 'Welcome to iReporter',
        'post flag': '/api/v1/redflag',
        'get flags': '/api/v1/redflags',
        'get flag': '/api/v1/redflag/flag_id',
        'alter flag': '/api/v1/redflag/flag_id',
        'update flag': '/api/v1/redflag/flag_id/key',
        'delete flag': '/api/v1/redflag/flag_id'
    }), 200


@app.route('/api/v1/redflags', methods=['POST'])
@jwt_required
def add_red_flag():
    data = request.get_json()
    user_id = get_jwt_identity()
    return red_flag_controller.create_incident(data, user_id, incident_type)


@app.route('/api/v1/redflags', methods=['GET'])
@jwt_required
def get_red_flags():
    user_id = get_jwt_identity()
    return red_flag_controller.get_all_incidents(user_id, incident_type)


@app.route('/api/v1/redflags/<int:flag_id>', methods=['GET'])
@jwt_required
def get_red_flag(flag_id):
    user_id = get_jwt_identity()
    return red_flag_controller.get_incident(flag_id, user_id, incident_type)


@app.route('/api/v1/redflags/<int:flag_id>', methods=['PUT'])
@jwt_required
def alter_red_flag(flag_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    return red_flag_controller.put_incident(
        data, flag_id, incident_type, user_id)


@app.route('/api/v1/redflags/<int:incident_id>/<string:query>',
           methods=['PATCH'])
@jwt_required
def update_red_flag_location(incident_id, query):
    data = request.get_json()
    user_id = get_jwt_identity()

    return red_flag_controller.patch_incident(
        data, incident_id, query, incident_type, user_id)


@app.route('/api/v1/redflags/<int:incident_id>', methods=['DELETE'])
@jwt_required
def delete_red_flag(incident_id):
    user_id = get_jwt_identity()
    return red_flag_controller.delete_incident(
        incident_id, user_id, incident_type)
