from flask.ext.via.routers.default import Functional, Pluggable
from flask.ext.via.routers import Include
from flask import render_template_string
from ortelius import app


def index():
    return render_template_string('Welcome to Ortelius v1!')


routes = [
    Functional('/', index),
    Include('ortelius.api_routes', url_prefix='/api/{version}'.format(version=app.config.get('API_VERSION')))
]
