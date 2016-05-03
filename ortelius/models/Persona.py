from ortelius import db
from ortelius.models.Date import Date
from ortelius.models.Hist_region import HistRegion, HistPlace
from ortelius.models.Process import Process
from ortelius.models.Fact import Fact


personas_hist_regions = db.Table('personas_hist_regions',
    db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id'))
    db.Column('persona_id', db.Integer, db.ForeignKey('persona.id')),
)

personas_hist_places = = db.Table('personas_hist_places',
    db.Column('hist_place_id', db.Integer, db.ForeignKey('hist_place.id'))
    db.Column('persona_id', db.Integer, db.ForeignKey('persona.id')),
)

personas_processes = = db.Table('personas_processes',
    db.Column('process_id', db.Integer, db.ForeignKey('process.id'))
    db.Column('persona_id', db.Integer, db.ForeignKey('persona.id')),
)

personas_facts = = db.Table('personas_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id'))
    db.Column('persona_id', db.Integer, db.ForeignKey('persona.id')),
)


class Persona(db.Model):
    """Persona model"""
    __tablename__ = 'persona'

    def __init__(self,
                 name = None
                 label = None
                 description = None
                 start_date = None
                 end_date = None
                 text = None
                 type = None
                 facts = None
                 hist_regions = None
                 hist_places = None
                 processes = None
                 trusted = False
                ):
        self.name = name
        self.label = label
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.text = text
        self.type = type
        self.facts = facts
        self.hist_regions = hist_regions
        self.hist_places = hist_places
        self.processes = processes
        self.trusted = trusted

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(255), nullable=False, unique=True)
    label         = db.Column(db.Unicode(255))
    description   = db.Column(db.UnicodeText, server_default='No description')
    start_date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    start_date    = db.relationship('Date', backref=db.backref('persona_starts', lazy='dynamic'), foreign_keys=start_date_id)
    end_date_id   = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    end_date      = db.relationship('Date', backref=db.backref('persona_ends', lazy='dynamic'), foreign_keys=end_date_id)
    text          = db.Column(db.UnicodeText, server_default='No text')
    type_name     = db.Column(db.String, db.ForeignKey('pers_type.name'), nullable=True)
    facts         = db.relationship('Fact', secondary=personas_facts, backref=db.backref('processes'), lazy='dynamic')
    hist_regions  = db.relationship('HistRegion', secondary=personas_hist_regions, backref=db.backref('processes'), lazy='dynamic')
    hist_places   = db.relationship('HistPlace', secondary=personas_hist_places, backref=db.backref('processes'), lazy='dynamic')
    processes     = db.relationship('Process', secondary=personas_processes, backref=db.backref('processes'), lazy='dynamic')
    trusted       = db.Column(db.Boolean)


class PersType(db.Model):
    """PersType model"""
    __tablename__ = 'pers_type'

    def __init__(name=None, label = None, personas = None):
        self.name = name
        self.label = label
        self.personas = personas

    name = db.Column(db.String(120), primary_key=True)
    label = db.Column(db.Unicode(120), nullable=False, unique=True)
    personas = db.relationship('Persona', backref=db.backref('type', uselist=False), lazy='dynamic')
