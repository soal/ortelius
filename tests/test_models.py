#!/usr/bin/env python3.4
import unittest
import datetime
import sqlalchemy

from ortelius.models.Date import Date
from ortelius.models.Coordinates import Coordinates, Quadrant, Shape


class TestDate(unittest.TestCase):

    def test_valid_data_creation(self):
        """Creating date with valid args"""
        self.assertIsInstance(Date.create(datetime.date.today()), Date)

    def test_invalid_data_creation(self):
        """Creating date with invalid args: no date kwarg and date kwarg is string instead of datetime.date"""
        self.assertRaises(sqlalchemy.exc.ArgumentError, callableObj=Date.create)
        self.assertRaises(sqlalchemy.exc.ArgumentError, callableObj=Date.create, date='1978')


class TestCoordinates(unittest.TestCase):

    def test_valid_coordinates_creation(self):
        """Creating coordinates with valid args"""
        self.assertIsInstance(Coordinates.create(90, -78.45678), Coordinates)

    def test_invalid_coordinates_creation(self):
        """Creating coordinates with invalid args, check for exceptions raising"""
        self.assertRaises(TypeError, callableObj=Coordinates.create)


class TestQuadrant(unittest.TestCase):

    def test_make_list(self):
        """Creating list of quadrant coordinates and store it in Quadrant class"""
        self.assertIsInstance(Quadrant.quadrants, list)
        self.assertGreater(len(Quadrant.quadrants), 0)

    def test_calc(self):
        """Calculate quadrant for given coordinates"""
        lat = -96
        long= 65.2334
        expectedList = [-96, 64]
        self.assertEqual(Quadrant.calc(lat, long), expectedList)


    def test_make_hash(self):
        """Making quadrant hash for given coordinates"""
        lat = 89.90
        long = -50.1
        expectedHash = '92,-52'
        self.assertEqual(Quadrant.make_hash(lat, long), expectedHash)


    def test_get(self):
        """Get quadrant for given coordinates"""
        lat = 89.90
        long = -50.1
        self.assertIsInstance(Quadrant.get(lat, long), Quadrant)
        self.assertEqual(Quadrant.get(lat, long).hash, '92,-52')


class TestFact(unittest.TestCase):
    # TODO: fact testing
    pass

# TODO: create tests for Coordinates model

# TODO: create tests for User model
# TODO: create tests for Fact model
