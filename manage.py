#!/usr/bin/env python3.4
import unittest
import coverage
import os

from flask.ext.script import Manager, Server
from flask_failsafe import failsafe
from flask.ext.migrate import Migrate, MigrateCommand

import create_initial_data
from ortelius import app, db

from ortelius.models.Collection import *
from ortelius.models.Coordinates import *
from ortelius.models.Date import *
from ortelius.models.Fact import *
from ortelius.models.Geo_region import *
from ortelius.models.Hist_region import *
from ortelius.models.Persona import *
from ortelius.models.Process import *
from ortelius.models.User import *

COV = coverage.coverage(
    branch=True,
    include='ortelius/*',
    omit=[
        'tests/*',
        'test_data/*',
        'create_initial_data',
        'ortelius/settings.py',
        'ortelius/*/__init__.py'
    ]
)
COV.start()

manager = Manager(app)


@failsafe
def create_app():
    return app

manager = Manager(create_app)
manager.add_command('runserver', Server())
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    os.environ['APP_SETTINGS'] = 'ortelius.settings.TestingConfig'
    app.config.from_object(os.environ['APP_SETTINGS'])
    create_db_schema()
    if not Quadrant.query.get('176,-176'):
        create_initial_data.create_quadrants()
    tests = unittest.TestLoader().discover('tests', pattern='*test*.py')
    result = unittest.TextTestRunner(verbosity=3).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    os.environ['APP_SETTINGS'] = 'ortelius.settings.TestingConfig'
    app.config.from_object(os.environ['APP_SETTINGS'])
    tests = unittest.TestLoader().discover('tests', pattern='*test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        try:
            COV.report()
        except coverage.misc.CoverageException as ce:
            print(ce)
        return 0
    else:
        return 1


@manager.command
def create_db_schema():
    """Creates the db tables."""
    os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.create_all()


@manager.command
def drop_db_schema():
    """Drops the db tables."""
    os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
    app.config.from_object(os.environ['APP_SETTINGS'])
    db.drop_all()


@manager.command
def create_admin():
    create_initial_data.create_admin()


@manager.command
def create_shape():
    create_initial_data.create_shape()



@manager.command
def create_processes():
    os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
    app.config.from_object(os.environ['APP_SETTINGS'])
    create_initial_data.create_processes()

@manager.command
def create_data():
    """Creates initial data."""
    os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
    app.config.from_object(os.environ['APP_SETTINGS'])
    create_initial_data.create_admin()
    create_initial_data.create_years()
    create_initial_data.create_quadrants()
    create_initial_data.create_facts()
    create_initial_data.create_hist_regions()
    create_initial_data.create_processes()

if __name__ == '__main__':
    manager.run()
