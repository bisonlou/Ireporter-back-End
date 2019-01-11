from api import app, jwt
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.controllers.user_controller import UserController

user_controller = UserController()


@app.route('/api/v1/register', methods=['POST'])
def register_user():
    data = request.get_json()
    return user_controller.register(data)


@app.route('/api/v1/login', methods=['POST'])
def login():
    auth = request.get_json()
    return user_controller.login(auth)


@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def get_all_users():
    user_id = get_jwt_identity()
    return user_controller.get_all(user_id)
