import json
from flask import Flask, Response, render_template, request
from datetime import date, datetime

import setup
from Service import Service

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/<term>/<start>/<end>', methods=['GET'])
def search_by_route(term, start, end):
    result = Service().search(
        term,
        datetime.strptime(start, '%Y-%m-%d'), 
        datetime.strptime(end, '%Y-%m-%d')
    )

    return json_response(result)

@app.route('/api/search', methods=['GET'])
def search_by_params():
    params = {
        'term': request.args.get('term', default = None, type = str),
        'start': request.args.get('start', default = None, type = str),
        'end': request.args.get('end', default = None, type = str)
    }

    for (k, value) in params.items():
        if value is None:
            raise ValueError('Parameter [{}] is required'.format(k))

    result = Service().search(
        params['term'],
        datetime.strptime(params['start'], '%Y-%m-%d'), 
        datetime.strptime(params['end'], '%Y-%m-%d')
    )

    return json_response(result)

def json_response(dict_obj):
    result_json = json.dumps(dict_obj, ensure_ascii=False).encode('utf8')
    return Response(result_json, mimetype='application/json')