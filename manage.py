#!/usr/bin/env python3
#
import os, sys, inspect, traceback
import unittest
import coverage
from sqlalchemy.engine import reflection
from sqlalchemy.schema import (
        MetaData,
        Table,
        DropTable,
        ForeignKeyConstraint,
        DropConstraint,
        )

from scripts import create_initial_data, shapes_processor
from ortelius import database, app

from ortelius.types.historical_date import *
from ortelius.models.Shape import *
from ortelius.models.Element import *
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
    conn=database.db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(database.db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((),(),name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


def create_data():
    """Creates initial data."""
    print('Creating test data...')
    os.environ['APP_SETTINGS'] = 'development'
    create_initial_data.create_admin(database.db)


def run():
    """Start development server"""
    os.system('hug -f ortelius/app.py')

# def create_shapes():
#     print('Creating shapes...')
#     if sys.argv[2]:
#         input_file = sys.argv[2]
#     else:
#         input_file = '/mnt/data/Map_Data/KLMs/selected/roman_republic.geojson'
    # shapes = shapes_processor.parse(HistoricalDate, Shape, Coordinates, Quadrant, Date, input_file)
    # for shape in shapes:
    #     database.db.session.add(shape)
    # database.db.session.commit()
    # print('Done!')

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
