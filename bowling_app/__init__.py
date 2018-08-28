from flask import Flask
from flask_restful import Api
from flask_cors import CORS

bowling = Flask(__name__)
bowling_api = Api(bowling)
cors = CORS(bowling, resources={r"/games/*": {"origins": "*"}})

# Games database
games = {}

from bowling_app import routes
from bowling_app import demo
