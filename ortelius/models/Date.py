import sqlalchemy
from ortelius import database
# import ortelius
from ortelius.types.historical_date import HistoricalDate, HDate

db = database.db


class Date(db.Model):
    """Date model"""
    __tablename__ = 'date'

    def __init__(self, date=None, year=None):
        self.date = date
        self.year = year

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(HDate, nullable=False, unique=True)
    year_number = db.Column(db.Integer, db.ForeignKey('year.number'), nullable=True)
    year = db.relationship('Year', backref=db.backref('dates', uselist=True, lazy='dynamic'))

    @classmethod
    def create(cls, date=None):
        """Create or get date if it's already exist. Date should be instance of datetime.datetime"""

        if not date:
            raise sqlalchemy.exc.ArgumentError('Fields required: date')
        if not isinstance(date, HistoricalDate):
            raise sqlalchemy.exc.ArgumentError('Date must be instance of HistoricalDate')


        new_date = db.query(cls).filter_by(date=date).first()
        if not new_date:
            year = db.query(Year).get(date.year)
            new_date = cls(date=date, year=year)
            db.session.add(new_date)

        return new_date


class Year(db.Model):
    """
        Year model. Contents year number as integer (e.g -879, 1678) and list of dates in this year.
        Note that year does not method have 'create' and should be created beforehand, not dynamically.
    """
    __tablename__ = 'year'

    def __init__(self, number=None, century=None):
        self.number = number
        self.century = century

    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    century_number = db.Column(db.Integer, db.ForeignKey('century.number'), nullable=True)
    century = db.relationship('Century', backref=db.backref('years', uselist=True, lazy='dynamic'))


class Century(db.Model):
    """
        Century model. Contents century number as integer (e.g -10, 19) and list of years in this century.
        Note that century does not method have 'create' and should be created beforehand, not dynamically.
    """
    __tablename__ = 'century'

    def __init__(self, number=None, millenium=None):
        self.number = number
        self.millenium = millenium

    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    millenium_number = db.Column(db.Integer, db.ForeignKey('millenium.number'), nullable=True)
    millenium = db.relationship('Millenium', backref=db.backref('centuries', uselist=True, lazy='dynamic'))


class Millenium(db.Model):
    """
        Millenium model. Contents millenimum number as integer (e.g -2, 1) and list of centuries in this millenimum.
        Note that millenium does not have method 'create' and should be created beforehand, not dynamically.
    """
    __tablename__ = 'millenium'

    def __init__(self, number=None):
        self.number = number

    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
