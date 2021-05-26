import json
import pathlib
from flask import Flask, Response, render_template, request
from datetime import datetime

from .setup import app_setup
from .service.Service import Service

app_setup()
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/api/<term>/<start>/<end>', methods=['GET'])
def search_by_route(term, start, end):
    result = search(term, start, end)
    return Response(result, mimetype='application/json')

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

    result = search(params['term'], params['start'], params['end'])
    return Response(result, mimetype='application/json')

@app.route('/api/post', methods=['POST'])
def analyse_post():
    result = analyzePost(request.form['texto'])

    return Response(result, mimetype='application/json')


def search(term, start, end):
    def cached_search():
        result = Service().search(
            term,
            datetime.strptime(start, '%Y-%m-%d'), 
            datetime.strptime(end, '%Y-%m-%d')
        )

        return json.dumps(result, ensure_ascii=False).encode('utf8')
    
    #return cache_in_file(cached_search, 'cache.json')
    return cached_search()

def analyzePost(post):
    result =  Service().analyzePost(post)
    return json.dumps(result, ensure_ascii=False).encode('utf8')


def cache_in_file(supplier, filename: str):
    filepath = pathlib.Path(__file__).parent.parent.parent.joinpath(filename)

    if filepath.exists():
       return filepath.read_bytes()

    value = supplier()

    with open(filepath, 'wb') as file:
        file.write(value)

    return value
