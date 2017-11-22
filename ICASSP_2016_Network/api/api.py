import os
from functools import wraps

import requests
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

auth_token = os.getenv('PN_AUTH_TOKEN')
db_connect_str = os.getenv('PN_DB_URI')

if not auth_token or not db_connect_str:
    raise ValueError('Missing PN_AUTH_TOKEN or PN_DB_CONNECT environment variables for configuration')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_connect_str
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args, **kwargs)) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)

    return decorated_function


@app.route('/get_phrase_data', methods=['GET', 'POST'])
@support_jsonp
def get_phrase_data():
    nid = int(request.args.get('nid'))
    with db.get_engine().begin() as connection:
        query = text('''
          SELECT file.mbid
               , file.raagaid
               , file.tonic
               , pattern.start_time as "start"
               , pattern.end_time as "end"
            FROM pattern
            JOIN file
              ON (file.id = pattern.file_id)
           WHERE pattern.id = :nid''')
        result = connection.execute(query, {'nid': nid})

        row = result.fetchone()

    return jsonify(**row)


@app.route('/get_rec_data', methods=['GET', 'POST'])
@support_jsonp
def get_rec_data():
    mbid = request.args.get('mbid')
    url = 'http://dunya.compmusic.upf.edu/api/carnatic/recording/{}'.format(mbid)
    data = requests.get(url, headers={'Authorization': 'Token {}'.format(auth_token)})
    return jsonify(**(data.json()))


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0')
