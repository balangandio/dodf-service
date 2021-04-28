from flask import Flask, Response, render_template
from datetime import date, datetime

app = Flask(__name__)

from Parameter import PeriodParameter, ParameterMap, spread_params_in_periods
from Client import Client
import json


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<term>/<start>/<end>', methods=['GET'])
def request(term, start, end):
    result = request(
        term,
        datetime.strptime(start, '%Y-%m-%d'), 
        datetime.strptime(end, '%Y-%m-%d')
    )
    result_json = json.dumps(result, ensure_ascii=False).encode('utf8')
    return Response(result_json, mimetype='application/json')


def request(term, start_date, end_date):
    client = Client()

    parameters = ParameterMap(term)
    params = spread_params_in_periods(parameters, start_date, end_date)

    collection = client.request_all_pages(params)

    return {
        'term': term,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'result': collection.to_dict()
    }