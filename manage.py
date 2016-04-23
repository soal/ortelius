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
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()

@manager.command
def create_facts():
    for f in test_facts:
        new_start_date = Date.create(date=datetime.datetime.strptime(f['start_date'], '%d-%m-%Y'))
        new_end_date = Date.create(date=datetime.datetime.strptime(f['end_date'], '%d-%m-%Y'))
        if f['coordinates']:
            point = Coordinates.create(f['coordinates'][0], f['coordinates'][1])
            db.session.add(point)

            new_shape = Shape(start_date=new_start_date, end_date=new_end_date, coordinates=[point])
            db.session.add(new_shape)

        new_fact = Fact(name = f['name'],
                        label=f['label'],
                        description=f['description'],
                        info=f['info'],
                        weight=f['weight'],
                        type=FactType.create(name=f['type'][0], label=f['type'][1]),
                        start_date=new_start_date,
                        end_date=new_end_date,
                        text=f['text'],
                        shape=new_shape
                       )
        db.session.add(new_fact)
        db.session.commit()

def create_shape():
    point = Coordinates.create(66.82, 10.5)
    sh = Shape(start_date=Date.create(date=datetime.date.today()), end_date=Date.create(date=datetime.date.today()), coordinates=[point])
    db.session.add(sh)
    db.session.commit()

def create_quadrants():
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
