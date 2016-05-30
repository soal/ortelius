from ortelius import database
from ortelius.models.Fact import Fact
from ortelius.models.Process import Process
from ortelius.models.Persona import Persona

db = database.db

collections_facts = db.Table('collections_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)
collections_processes = db.Table('collections_processes',
    db.Column('process_id', db.Integer, db.ForeignKey('process.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)
collections_personas = db.Table('collections_personas',
    db.Column('persona_id', db.Integer, db.ForeignKey('persona.id')),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'))
)


class Collection(db.Model):
    """Collection model"""
    __tablename__ = 'collection'

    def __init__(self, name=None, label=None, facts=[], processes=[], personas=[]):
        self.name = name
        self.label = label
        self.processes = processes
        self.personas = personas

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False, unique=True)
    label       = db.Column(db.Unicode(255))
    facts       = db.relationship('Fact', secondary=collections_facts, lazy='dynamic')
    processes   = db.relationship('Process', secondary=collections_processes, lazy='dynamic')
    personas    = db.relationship('Persona', secondary=collections_personas, lazy='dynamic')
