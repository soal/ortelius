import os
from sqlalchemy_wrapper import SQLAlchemy
import settings

try:
    env = os.environ['APP_SETTINGS']
except:
    env = os.environ['APP_SETTINGS'] = 'development'

if env == 'development':
    config = settings.DevelopmentConfig


db = SQLAlchemy(config.SQLALCHEMY_DATABASE_URI)
