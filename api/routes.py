from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
import run

app = Flask(__name__)


red_flags = [
    {       
            'id': 1,
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'description': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        },
    {
            'id': 2,
            'date': '2018-12-24',
            'offender': 'Police Officer',
            'description': 'Police officer at CPS Badge #162',
            'location': '(-65.712557, -15.000182)',
            'image': 'photo_0979.jpg',
            'video': 'mov_0987.mp4'
        }
]


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello world'})


@app.route('/api/v1/redflag', methods=['POST'])
def add_red_flag():

    data = request.get_json()
    date = data.get('date')
    offender = data.get('offender')
    description = data.get('description')
    location = data.get('location')
    image = data.get('image')
    video = data.get('video')

    if 'offender' not in data:
        return jsonify({'Error': error}), 400
    if 'location' not in data:
        return jsonify({'Error': error}), 400
    if 'description' not in data:
        return jsonify({'Error': error}), 400

    return jsonify({'message': [data]}), 201


@app.route('/api/v1/redflags', methods=['GET'])
def get_red_flags():
    return jsonify({'Redflags': [red_flags]})
