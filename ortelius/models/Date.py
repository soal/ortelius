import math
from ortelius import db


class Date(db.Model):
    """Date model"""
    __tablename__ = 'date'

    def __init__(self, date=None, year=None, year_number=None):
        self.date = date
        # self.year = year
        self.year_number = year_number

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    year_number = db.Column(db.Integer, db.ForeignKey('year.number'), nullable=True)
    # year is declared in Year class via backref
    # hist_regions is declared in HistRegion class via backref


class Year(db.Model):
    """Year model"""
    __tablename__ = 'year'

    def __init__(self, number=None, dates=None, century=None, century_number=None):
        self.number = number
        # self.century = century
        self.century_number = century_number
        if dates:
            self.dates = dates

    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    dates = db.relationship('Date', backref=db.backref('year', lazy='select'), lazy='dynamic')
    century_number = db.Column(db.Integer, db.ForeignKey('century.number'), nullable=True)
    # century is declared in Century class via backref

    # def calculate_century(self):
    #     return math.floor(self.number / 100) if (self.number / 100) < 0 else math.floor(self.number / 100) + 1


class Century(db.Model):
    """Century model"""
    __tablename__ = 'century'

    def __init__(self, number=None, years=None, millenium=None, millenium_number=None):
        self.number = number
        # self.millenium = millenium
        self.millenium_number = millenium_number
        if years:
            self.years = years

    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    years = db.relationship('Year', backref=db.backref('century'), lazy='dynamic')
    millenium_number = db.Column(db.Integer, db.ForeignKey('millenium.number'), nullable=True)
    # millenium is declared in Millenium class via backref

    # def calculate_millenium(self):
    #     return math.floor(self.number / 10) if (self.number / 10) < 0 else math.floor(self.number / 10) + 1


class Millenium(db.Model):
    """Millenium model"""
    __tablename__ = 'millenium'

    def __init__(self, number=None, centuries=None):
        self.number = number
        if centuries:
            self.centuries = centuries

    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    centuries = db.relationship('Century', backref=db.backref('millenium'), lazy='dynamic')
