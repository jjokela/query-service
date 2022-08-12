import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# @app.route('/')
# def home():
#     return render_template('index.html')


@app.get('/health')
def health():
    return 'OK'


countries = [
    {'id': 1, 'name': 'United States', 'code': 'US'},
    {'id': 2, 'name': 'Canada', 'code': 'CA'},
    {'id': 3, 'name': 'Mexico', 'code': 'MX'},
    {'id': 4, 'name': 'United Kingdom', 'code': 'UK'},
    {'id': 5, 'name': 'France', 'code': 'FR'}
]

def _find_next_id():
    return max(country["id"] for country in countries) + 1


@app.get('/')
def healthcheck():
    return jsonify('OK')


@app.get('/countries')
def get_countries():
    return jsonify(countries)


@app.post('/countries')
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201

    return {"error": "Request must be in JSON"}, 415


@app.post('/search')
@cross_origin()
def find_metrics():
    with open('data/series.json', 'r') as f:
        data = json.load(f)
        return data


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
