import unittest
from datetime import datetime

from ortelius.ortelius.types.historical_date import HistoricalDate

class TestHistoricalDate(unittest.TestCase):
    def test_creation_from_string(self):
        date = '1453-5-29'
        self.assertEqual(HistoricalDate(date).year, '1453')
        self.assertEqual(HistoricalDate(date).month, '05')
        self.assertEqual(HistoricalDate(date).day, '29')

    def test_creation_from_int(self):
        date = 14530529
        self.assertEqual(HistoricalDate(date).year, '1453')
        self.assertEqual(HistoricalDate(date).month, '05')
        self.assertEqual(HistoricalDate(date).day, '29')

    def test_creation_from_datetime(self):
        date = datetime.strptime('1453-5-29', '%Y-%m-%d')
        self.assertEqual(HistoricalDate(date).year, '1453')
        self.assertEqual(HistoricalDate(date).month, '05')
        self.assertEqual(HistoricalDate(date).day, '29')

    def test_equal(self):
        first_date = HistoricalDate('1453-5-29')
        second_date = HistoricalDate(14530529)
        third_date = HistoricalDate('1917-11-7')

        self.assertTrue(first_date == second_date)
        self.assertFalse(first_date == third_date)

    def test_greater(self):
        first_date = HistoricalDate('1453-5-29')
        second_date = HistoricalDate('1917-11-7')

        self.assertTrue(second_date > first_date)


    def test_greater_equal(self):
        first_date = HistoricalDate('1453-5-29')
        second_date = HistoricalDate(14530529)
        third_date = HistoricalDate('1917-11-7')

        self.assertTrue(third_date >= first_date)
        self.assertTrue(second_date >= first_date)

    def test_lesser(self):
        first_date = HistoricalDate('1453-5-29')
        second_date = HistoricalDate('1917-11-7')

        self.assertTrue(first_date < second_date)

    def test_lesser_equal(self):
        first_date = HistoricalDate('1453-5-29')
        second_date = HistoricalDate(14530529)
        third_date = HistoricalDate('1917-11-7')

        self.assertTrue(first_date <= third_date )
        self.assertTrue(first_date <= second_date)

    def test_to_string(self):
        date = '1453-05-29'
        self.assertEqual(HistoricalDate(date).to_string(), date)

    def test_to_julian(self):
        julian_date = '1917-10-25'
        gregorian_date = HistoricalDate('1917-11-7')

        self.assertEqual(gregorian_date.to_julian(), julian_date)
