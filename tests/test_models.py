#!/usr/bin/env python3.4
import unittest
import datetime
import sqlalchemy

from ortelius.models.Date import Date



class DateTest(unittest.TestCase):
    def __init__(self):
        super(DateTest, self).__init__()

    def valid_data_creation(self):
        self.assertIsInstance(Date.create(datetime.date.today()), Date)

    def invalid_data_creation(self):
        self.assertRaises(sqlalchemy.exc.ArgumentError, callableObj=Date.create())  # date kwarg is required to create Date
        self.assertRaises(sqlalchemy.exc.ArgumentError, callableObj=Date.create(date='1978'))  # date kwarg must be datetime object


if __name__ == "__main__":
    unittest.main()