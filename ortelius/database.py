import os
import settings
from sqlalchemy_wrapper import SQLAlchemy

try:
    env = os.environ['APP_SETTINGS']
except:
    env = os.environ['APP_SETTINGS'] = 'development'
if env == 'testing':
    config = settings.TestingConfig
elif env == 'production':
    config = settings.ProductionConfig
elif env == 'staging':
    config = settings.StagingConfig
else:
    config = settings.DevelopmentConfig


db = SQLAlchemy(config.SQLALCHEMY_DATABASE_URI)
