from ortelius import database
from ortelius.models.Coordinates import Shape
from ortelius.models.Date import Date
from ortelius.models.Fact import Fact

db = database.db

hist_regions_facts = db.Table('hist_regions_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id'))
)

hist_places_facts = db.Table('hist_places_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('hist_place_id', db.Integer, db.ForeignKey('hist_place.id'))
)

hist_regions_hist_places = db.Table('hist_regions_hist_places',
    db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id')),
    db.Column('hist_place_id', db.Integer, db.ForeignKey('hist_place.id'))
)

Shape.hist_region_id = db.Column(db.Integer, db.ForeignKey('hist_region.id'))
Shape.hist_place_id = db.Column(db.Integer, db.ForeignKey('hist_place.id'))


class HistRegion(db.Model):
    """HistRegion model"""
    __tablename__ = 'hist_region'

    def __init__(self,
                 name=None,
                 label=None,
                 description=None,
                 text=None,
                 start_date=None,
                 end_date=None,
                 facts=[],
                 shapes=[],
                 trusted=False):
        self.name        = name
        self.label       = label
        self.description = description
        self.text        = text
        self.start_date  = start_date
        self.end_date    = end_date
        self.facts       = facts
        self.shapes      = shapes
        self.trusted     = trusted

    id              = db.Column(db.Integer, primary_key=True)
    text            = db.Column(db.UnicodeText, server_default="No text")
    name            = db.Column(db.String(255), nullable=False, unique=True)
    label           = db.Column(db.Unicode(255))
    description     = db.Column(db.UnicodeText, server_default="No description")
    start_date_id   = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    start_date      = db.relationship('Date', backref=db.backref('hist_regions_start', lazy='joined'), foreign_keys=start_date_id)
    end_date_id     = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    end_date        = db.relationship('Date', backref=db.backref('hist_regions_end', lazy='joined'), foreign_keys=end_date_id)
    shapes          = db.relationship('Shape', backref=db.backref('hist_region'), lazy='dynamic')
    mark            = db.relationship('Shape')
    facts           = db.relationship('Fact', secondary=hist_regions_facts, backref=db.backref('hist_regions'), lazy='dynamic')
    next_region_id  = db.Column(db.Integer, db.ForeignKey('hist_region.id'), nullable=True)
    prev_region_id  = db.Column(db.Integer, db.ForeignKey('hist_region.id'), nullable=True)
    next_region     = db.relationship('HistRegion', backref=db.backref('prev_region', uselist=False), uselist=False, foreign_keys=next_region_id, remote_side='HistRegion.id')
    hist_places     = db.relationship('HistPlace', secondary=hist_regions_hist_places, backref=db.backref('hist_regions'), lazy='dynamic')
    trusted         = db.Column(db.Boolean)

    def create_mark(self, dots):
        # TODO: Mark creation
        mark = None
        self.mark = mark


class HistPlace(db.Model):
    """HistPlace model"""
    __tablename__ = 'hist_place'

    def __init__(self,
                 name=None,
                 label=None,
                 description=None,
                 text=None,
                 start_date=None,
                 end_date=None,
                 facts=None,
                 trusted=False):
        self.name        = name
        self.label       = label
        self.description = description
        self.text        = text
        self.start_date  = start_date
        self.end_date    = end_date
        self.facts       = facts
        self.trusted     = trusted

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(255), nullable=False, unique=True)
    label         = db.Column(db.Unicode(255))
    description   = db.Column(db.UnicodeText, server_default="No description")
    text          = db.Column(db.UnicodeText, server_default="No text")
    start_date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    start_date    = db.relationship('Date', backref=db.backref('hist_place_start', lazy='joined'), foreign_keys=start_date_id)
    end_date_id   = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    end_date      = db.relationship('Date', backref=db.backref('hist_place_end', lazy='joined'), foreign_keys=end_date_id)
    shapes        = db.relationship('Shape', backref=db.backref('hist_place'), lazy='dynamic')
    facts         = db.relationship('Fact', secondary=hist_places_facts, backref=db.backref('hist_places'), lazy='dynamic')
    trusted       = db.Column(db.Boolean)
