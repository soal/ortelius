import os
import hug

from ortelius.api import Dicts, Elements, Shapes
from ortelius import settings

try:
    env = os.environ['APP_SETTINGS']
except:
    env = os.environ['APP_SETTINGS'] = 'development'

if env == 'testing':
    config = settings.TestingConfig
elif env == 'production':
    config = settings.ProductionConfig
else:
    config = settings.DevelopmentConfig


@hug.get('/')
def welcome():
    return 'Welcome to ortelius version {0}'.format(config.API_VERSION)

@hug.extend_api('/objects')
def get_data():
    return [Elements, Shapes]

@hug.extend_api('/dicts')
def get_dicts():
    return [Dicts]


if __name__ == '__main__':
    welcome.interface.cli()
