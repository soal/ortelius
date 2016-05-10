import os
from flask import Flask, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from flask.ext.via import Via

__all__ = ['make_json_app']

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.keys():
        app.error_handler_spec[None][code] = make_json_error

    return app

app = make_json_app(__name__)

try:
    os.environ['APP_SETTINGS']
except:
     os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'


app.config.from_object(os.environ['APP_SETTINGS'])
app.config.update({'VIA_ROUTES_MODULE': 'ortelius.routes'})

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)

# Setup Flask-Via routes pulgin
via = Via()

via.init_app(app, route_module='ortelius.routes')
