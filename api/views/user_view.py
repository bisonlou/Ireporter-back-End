from api import app, jwt
from flask_jwt_extended import jwt_required
from api.controllers.user_controller import UserController

user_controller = UserController()


@app.route('/api/v1/register', methods=['POST'])
def register_user():

    return user_controller.register()


@app.route('/api/v1/login', methods=['POST'])
def login():

    return user_controller.login()


@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def get_all_users():

    return user_controller.get_all()
