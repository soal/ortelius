#!/usr/bin/env python3
import unittest
import coverage
import traceback
import os, sys, inspect

from scripts import create_initial_data
from ortelius import database, app

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
        'scripts/*',
        'ortelius/settings.py',
        'ortelius/*/__init__.py'
    ]
)
COV.start()

# manager = Manager(create_app)
# manager.add_command('runserver', Server())
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)


def test():
    """Runs the unit tests without coverage."""
    os.environ['APP_SETTINGS'] = 'testing'
    create_db()
    if not database.db.query(Quadrant).get('176,-176'):
        create_initial_data.create_quadrants()
    tests = unittest.TestLoader().discover('tests', pattern='*test*.py')
    result = unittest.TextTestRunner(verbosity=3).run(tests)
    if result.wasSuccessful():
        os.environ['APP_SETTINGS'] = 'development'
        return 0
    else:
        os.environ['APP_SETTINGS'] = 'development'
        return 1

def cov():
    """Runs the unit tests with coverage."""
    os.environ['APP_SETTINGS'] = 'testing'
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
        os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
        app.config.from_object(os.environ['APP_SETTINGS'])
        return 0
    else:
        os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
        app.config.from_object(os.environ['APP_SETTINGS'])
        return 1

def create_db():
    """Creates the db tables."""
    os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
    # app.config.from_object(os.environ['APP_SETTINGS'])
    database.db.create_all()

def drop_db():
    """Drops the db tables."""
    os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
    # app.config.from_object(os.environ['APP_SETTINGS'])
    database.db.drop_all()


# def create_admin():
#     create_initial_data.create_admin()
#
# def create_shape():
#     create_initial_data.create_shape()



# def create_processes():
#     os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
#     # app.config.from_object(os.environ['APP_SETTINGS'])
#     create_initial_data.create_processes()
#
# def create_personas():
#     os.environ['APP_SETTINGS'] = 'ortelius.settings.DevelopmentConfig'
#     # app.config.from_object(os.environ['APP_SETTINGS'])
#     create_initial_data.create_personas()
#
def create_data():
    """Creates initial data."""
    print('Creating test data...')
    os.environ['APP_SETTINGS'] = 'development'
    create_initial_data.create_admin(database.db)
    create_initial_data.create_years(database.db)
    create_initial_data.create_quadrants(database.db)
    create_initial_data.create_facts(database.db)
    create_initial_data.create_hist_regions(database.db)
    create_initial_data.create_processes(database.db)
    create_initial_data.create_personas(database.db)

def main():
    funcs = [x[0] for x in inspect.getmembers(sys.modules[__name__], inspect.isfunction)]
    funcs.pop(funcs.index('main'))
    if len(sys.argv) < 2:
        print('Not enough arguments. Please, tell me what to do. Available arguments: {0}'.format(', '.join(funcs)))
        return 1
    first_arg = sys.argv[1]
    if first_arg in funcs:
        try:
            globals()[first_arg]()
        except Exception as e:
            print(traceback.print_tb(sys.exc_info()[2]))
            print(e)
            return 1
    else:
        print('Wrong argument: "{0}". Available arguments: {1}'.format(first_arg, ', '.join(funcs)))
        return 1
    return 0


if __name__ == '__main__':
    main()
