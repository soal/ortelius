#!/usr/bin/env python3.4
import unittest
import coverage
import os

import sqlalchemy
from flask.ext.script import Manager, Server
from flask_failsafe import failsafe
from flask.ext.migrate import Migrate, MigrateCommand

from ortelius import app, db
from ortelius.models.Coordinates import *
from ortelius.models.Date import *
from ortelius.models.Fact import *
from ortelius.models.Hist_region import *
from ortelius.models.User import *

from test_data.test_facts import test_facts

COV = coverage.coverage(
    branch=True,
    include='ortelius/*',
    omit=[
        'ortelius/tests/*',
        'ortelius/config.py',
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
    db.create_all()


@manager.command
def drop_db_schema():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_admin():
    """Creates the admin user."""
    admin_role = Role(id=1, name='admins', label='Administrators')
    admin_user = User(id=1, username='admin',
                      email='ad@min.com', password='admin', active=True)
    admin_user_role = UsersRoles(user_id=admin_user.id, role_id=admin_role.id)
    db.session.add(admin_role)
    db.session.add(admin_user)
    db.session.commit()
    db.session.add(admin_user_role)
    db.session.commit()

@manager.command
def create_years():
    # Create millenimus, centuries and years from -5000 to 2999
    for i in (-5, -4, -3, -2, -1, 1, 2, 3):
        print('Create millenium: ' + str(i))
        mil = Millenium(number=i)
        db.session.add(mil)
        for j in range(0, 10):
            centNumber = j+(i*10) if i < 0 else j + 1 + ((i-1)*10)
            cent = Century(number=centNumber, millenium=mil)
            db.session.add(cent)
            for k in range(0, 100):
                yearNumber = k+(centNumber*100) - 1 if i < 0 else k + ((centNumber-1)*100)
                year = Year(number=yearNumber, century=cent)
                db.session.add(year)

    db.session.commit()

@manager.command
def create_fact_types():
    f_types = [
                ['battle', 'сражение'],
                ['peace treaty', 'мирный договор']
              ]

    for t in f_types:
        new_type = FactType(name=t[0], label=t[1])
        db.session.add(new_type)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            print("INFO: Cannot create row: key already exist")
            db.session.rollback()

@manager.command
def create_facts():
    create_fact_types()
    for f in test_facts:
        Quadrant.make_list()
        if f['coordinates']:
            dot = Coordinates(lat=f['coordinates'][0],
                              long=f['coordinates'][1],
                              quadrant_hash=Quadrant.make_hash(f['coordinates'][0], f['coordinates'][1]))
            db.session.add(dot)
            new_shape = Shape(coordinates=[dot])
            db.session.add(new_shape)
        new_fact = Fact(name = f['name'],
                    label=f['label'],
                    description=f['description'],
                    info=f['info'],
                    weight=f['weight'],
                    type_id=FactType.query.filter_by(name=f['type'][0]).all()[0].id,
                    start_date=f['start_date'],
                    end_date=f['end_date'],
                    text=f['text'],
                    shape=new_shape
                   )
        db.session.add(new_fact)
    db.session.commit()

@manager.command
def create_shape():
    Quadrant.make_list()
    point = Coordinates.create(66.80, -90.5)
    sh = Shape(start_date=Date.create(date=datetime.date.today()), end_date=Date.create(date=datetime.date.today()), coordinates=[point])
    db.session.add(sh)
    db.session.commit()

@manager.command
def create_quadrants():
    Quadrant.make_list()
    for q in Quadrant.quadrants:
        quadrant = Quadrant(hash=Quadrant.make_hash(q[0], q[1]))
        db.session.add(quadrant)
    db.session.commit()


@manager.command
def create_initial_data():
    """Creates initial data."""
    create_admin()
    create_years()
    create_quadrants()

if __name__ == '__main__':
    manager.run()
