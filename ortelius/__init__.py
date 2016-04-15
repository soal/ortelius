import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS

from flask.ext.via import Via

app = Flask(__name__)
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

# from handymap.server.models import User
