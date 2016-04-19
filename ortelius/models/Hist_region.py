from ortelius import db
from ortelius.models.Coordinates import Shape
from ortelius.models.Date import Date
from ortelius.models.Fact import Fact

hist_regions_facts = db.Table(
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id'))
)


class Hist_region(db.Model):
    """Hist_region model"""
    __tablename__ = 'hist_region'

    def __init__(self,
                 name=None,
                 label=None,
                 description=None,
                 start_date=None,
                 end_date=None,
                 facts=None
                 shapes=None):
        self.name = name
        self.label = label
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.facts = facts
        self.shapes = shapes

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    label = db.Column(db.Unicode(255))
    description = db.Column(db.UnicodeText, server_default="No description")
    start_date = db.Column(db.Integer, db.ForeignKey('date.id'))
    end_date = db.Column(db.Integer, db.ForeignKey('date.id'))
    shapes = db.relationship('Shape', backref=db.backref('hist_region', lazy='dynamic') lazy='dynamic')
    facts = db.relationship('Fact', lazy='dynamic')
    # processes is declared in Process model via backref
