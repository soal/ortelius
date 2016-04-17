#!/usr/bin/env python

import unittest
import coverage
import datetime

from flask.ext.script import Manager, Server
from flask_failsafe import failsafe
from flask.ext.migrate import Migrate, MigrateCommand

from ortelius import app, db
from ortelius.models.User import User, Role, UsersRoles
from ortelius.models.Date import Millenium, Century, Year


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
manager.add_command('migrations', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='*test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
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
def create_db():
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
def create_initial_data():
    """Creates initial data."""
    # years = []
    # centuries = []
    # milleniums = []

    for i in (-5, -4, -3, -2, -1, 1, 2, 3):
        mil = Millenium(number=i)
        db.session.add(mil)
        print('mil: ' + str(i))
        for j in range(0, 10):
            centNumber = j+(i*10) if i < 0 else j + 1 + ((i-1)*10)
            cent = Century(number=centNumber, millenium_number=i)
            db.session.add(cent)
            print('cent: ' + str(centNumber))
            for k in range(0, 100):
                yearNumber = k+(centNumber*100) - 1 if i < 0 else k + ((centNumber-1)*100)
                year = Year(yearNumber, century_number=centNumber)
                print('year: ' + str(yearNumber))
                db.session.add(year)
                # years.append(year)

    db.session.commit()

if __name__ == '__main__':
    manager.run()
