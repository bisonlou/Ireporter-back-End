from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bison'

jwt = JWTManager(app)
test_client = app.test_client()

import api.views.red_flag_view
import api.views.user_view
import api.views.intervention_view
