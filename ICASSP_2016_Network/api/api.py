from __future__ import unicode_literals

from functools import wraps

import psycopg2 as psy
import requests
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS

auth_token = "31fbb43414dedad8a9e9b4379be1a6c8992849b4"

app = Flask(__name__)
CORS(app)

con = psy.connect(database='ICASSP2016_10RAGA_2S', user='sankalp')
cur = con.cursor()


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
    cmd = "select file.mbid, file.raagaid, file.tonic, pattern.start_time, pattern.end_time from pattern join file on (file.id = pattern.file_id) where pattern.id = %d"
    cur.execute(cmd%(nid))
    mbid, raaga, tonic, start, end = cur.fetchone()
    out = {'mbid':mbid, 'ragaid': raaga, 'start':start, 'end':end, 'tonic': tonic}

    return jsonify(**out)


@app.route('/get_rec_data', methods=['GET', 'POST'])
@support_jsonp
def get_rec_data():
    mbid = request.args.get('mbid')
    url = "http://dunya.compmusic.upf.edu/api/carnatic/recording/" + mbid
    data = requests.get(url, headers = {"Authorization":"Token " + auth_token})
    return jsonify(**(data.json()))


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host= '0.0.0.0', debug = True)
