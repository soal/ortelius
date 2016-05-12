from ortelius import database
from ortelius.models.Fact import Fact
from ortelius.models.Coordinates import Shape
from ortelius.models.Hist_region import HistRegion, HistPlace
from ortelius.models.Date import Date

db = database.db

processes_facts = db.Table('processes_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('process_id', db.Integer, db.ForeignKey('process.id'))
)

processes_hist_regions = db.Table('processes_hist_regions',
    db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id')),
    db.Column('process_id', db.Integer, db.ForeignKey('process.id'))
)

processes_hist_places = db.Table('processes_hist_places',
    db.Column('hist_place_id', db.Integer, db.ForeignKey('hist_place.id')),
    db.Column('process_id', db.Integer, db.ForeignKey('process.id'))
)

processes_subprocesses = db.Table('processes_subprocesses',
    db.Column('parent_id', db.Integer, db.ForeignKey('process.id')),
    db.Column('child_id', db.Integer, db.ForeignKey('process.id'))
)

Shape.processes_id = db.Column(db.Integer, db.ForeignKey('process.id'))

class Process(db.Model):
    """Process model"""
    __tablename__ = 'process'

    def __init__(self,
                 name = None,
                 label = None,
                 description = None,
                 start_date = None,
                 end_date = None,
                 shapes = [],
                 text = None,
                 type = None,
                 facts = [],
                 hist_regions = [],
                 hist_places = [],
                 subprocesses = [],
                 trusted = False
                ):
        self.name = name
        self.label = label
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.shapes = shapes
        self.text = text
        self.type = type
        self.facts = facts
        self.hist_regions = hist_regions
        self.hist_places = hist_places
        self.subprocesses = subprocesses
        self.trusted = trusted

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(255), nullable=False, unique=True)
    label             = db.Column(db.Unicode(255))
    description       = db.Column(db.UnicodeText, server_default='No description')
    start_date_id     = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    start_date        = db.relationship('Date', backref=db.backref('processes_starts', lazy='dynamic'), foreign_keys=start_date_id)
    end_date_id       = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    end_date          = db.relationship('Date', backref=db.backref('processes_ends', lazy='dynamic'), foreign_keys=end_date_id)
    shapes            = db.relationship('Shape', backref=db.backref('process', uselist=False))
    text              = db.Column(db.UnicodeText, server_default='No text')
    type_name         = db.Column(db.String, db.ForeignKey('process_type.name'), nullable=True)
    facts             = db.relationship('Fact', secondary=processes_facts, backref=db.backref('processes'), lazy='dynamic')
    hist_regions      = db.relationship('HistRegion', secondary=processes_hist_regions, backref=db.backref('processes'), lazy='dynamic')
    hist_places       = db.relationship('HistPlace', secondary=processes_hist_places, backref=db.backref('processes'), lazy='dynamic')
    subprocesses      = db.relationship('Process',
                                        secondary=processes_subprocesses,
                                        primaryjoin=id==processes_subprocesses.c.parent_id,
                                        secondaryjoin=id==processes_subprocesses.c.child_id,
                                        backref="parent_processes")

    trusted           = db.Column(db.Boolean)

    def __repr__(self):
        return '<Process %r, shows as %r>' % (self.name, self.label)


class ProcessType(db.Model):
    """ProcessType model"""
    __tablename__ = 'process_type'

    def __init__(self, name=None, label=None, processes=[]):
        self.name = name
        self.label = label
        self.processes = processes

    name = db.Column(db.String(120), primary_key=True)
    label = db.Column(db.Unicode(120), nullable=False, unique=True)
    processes = db.relationship('Process', backref=db.backref('type', uselist=False), lazy='dynamic')

    @classmethod
    def create(cls, name=None, label=None):
        new_type = cls.query.get(name)
        if not new_type:
            new_type = cls(name=name, label=label)
            db.session.add(new_type)

        return new_type

    def __repr__(self):
        return '<Process type %r, shows as %r>' % (self.name, self.label)
