#!/usr/bin/env python3.4
import unittest
import datetime
import sqlalchemy
from ortelius import db
from ortelius.types.historical_date import HistoricalDate as hd

from ortelius.types.historical_date import HistoricalDate
from ortelius.models.Date import Date
from ortelius.models.Coordinates import Coordinates, Quadrant, Shape
from ortelius.models.Fact import Fact, FactType
from ortelius.models.Process import ProcessType
from ortelius.models.Persona import PersType
from ortelius.models.Hist_region import HistRegion, HistPlace


class TestDate(unittest.TestCase):
    def test_valid_date_creation(self):
        """Creating date with valid args"""
        self.assertIsInstance(Date.create(hd(datetime.datetime.today())), Date)
        self.assertEqual(Date.create(hd(datetime.datetime.today())).date.year, hd(datetime.datetime.today()).year)

    def test_invalid_date_creation(self):
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

class TestFacts(unittest.TestCase):
    def test_fact_type_creation(self):
        self.assertEqual(FactType.create(name='battle', label='сражение').name, 'battle')


class TestProcess(unittest.TestCase):
    def test_process_type_creation(self):
        self.assertEqual(ProcessType.create(name='war', label='война').name, 'war')

class TestPersona(unittest.TestCase):
    def test_persona_type_creation(self):
        self.assertEqual(PersType.create(name='ruler', label='правитель').name, 'ruler')
