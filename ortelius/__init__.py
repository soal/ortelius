import os
from flask import Flask, render_template, url_for, send_file, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask_wtf.csrf import CsrfProtect

from flask.ext.via import Via



app = Flask(
    __name__,
    template_folder='templates',
    static_folder='../static'
)
try:
    os.environ['APP_SETTINGS']
except:
     os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'


app.config.from_object(os.environ['APP_SETTINGS'])
app.debug = True

app.jinja_env.globals['static'] = (
    lambda filename: url_for('static', filename = filename)
)
app.config.update({'VIA_ROUTES_MODULE': 'ortelius.routes'})

if app.testing:
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF checks while testing

db = SQLAlchemy(app)

# Setup Flask-Via routes pulgin
via = Via()
via.init_app(app, route_module='ortelius.routes')

# Setup Flask-Mail
mail = Mail(app)

# Setup WTForms CsrfProtect
CsrfProtect(app)

# Define bootstrap_is_hidden_field for flask-bootstrap's bootstrap_wtf.html
from wtforms.fields import HiddenField

def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)



# from handymap.server.models import User
