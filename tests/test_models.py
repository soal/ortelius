#!/usr/bin/env python3.4
import unittest
import datetime
import sqlalchemy

from ortelius.models.Date import Date


class TestDate(unittest.TestCase):

    def test_valid_data_creation(self):
        """Creating date table with valid args"""
        self.assertIsInstance(Date.create(datetime.date.today()), Date)

    def test_invalid_data_creation(self):
        """Creating date table with invalid args: no date kwarg and date kwarg is string instead of datetime.date"""
        self.assertRaises(sqlalchemy.exc.ArgumentError, callableObj=Date.create)
        self.assertRaises(sqlalchemy.exc.ArgumentError, callableObj=Date.create, date='1978')
