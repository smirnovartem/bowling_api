from flask import Flask
from flask_restful import Api

bowling = Flask(__name__)
bowling_api = Api(bowling)

games = {}

from bowling_app import routes
