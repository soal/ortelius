from ortelius import db
from ortelius.models.Fact import Fact
from ortelius.models.Hist_region import HistRegion, HistPlace
from ortelius.models.Process import Process
from ortelius.models.Coordinates import Shape


geo_regions_hist_regions = db.Table('geo_regions_hist_regions',
    db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id')),
    db.Column('geo_region_id', db.Integer, db.ForeignKey('geo_region.id'))
)

geo_regions_hist_places = db.Table('geo_regions_hist_places',
    db.Column('hist_place_id', db.Integer, db.ForeignKey('hist_place.id')),
    db.Column('geo_region_id', db.Integer, db.ForeignKey('geo_region.id'))
)

geo_regions_processes = db.Table('geo_regions_processes',
    db.Column('process_id', db.Integer, db.ForeignKey('process.id')),
    db.Column('geo_region_id', db.Integer, db.ForeignKey('geo_region.id'))
)

geo_regions_facts = db.Table('geo_regions_facts',
    db.Column('fact_id', db.Integer, db.ForeignKey('fact.id')),
    db.Column('geo_region_id', db.Integer, db.ForeignKey('geo_region.id'))
)

geo_regions_sub_geo_regions = db.Table('georegions_subgeoregions',
    db.Column('parent_id', db.Integer, db.ForeignKey('geo_region.id')),
    db.Column('child_id', db.Integer, db.ForeignKey('geo_region.id'))
)


class GeoRegion(db.Model):
    """GeoRegion model"""
    __tablename__ = 'geo_region'

    def __init__(self,
                 name = None,
                 label = None,
                 shape = None,
                 facts = [],
                 parent_regions = [],
                 child_regions = []
                ):
        self.name = name,
        self.label = label,
        self.shape = shape,
        self.facts = facts,
        self.parent_regions = parent_regions,
        self.child_regions = child_regions

    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(255), nullable=False, unique=True)
    label               = db.Column(db.Unicode(255))
    shape_id            = db.Column(db.Integer, db.ForeignKey('shape.id'), nullable=True)
    shape               = db.relationship('Shape', backref=db.backref('geo_region', uselist=False), uselist=False)
    hist_regions        = db.relationship('HistRegion', secondary=geo_regions_hist_regions, backref=db.backref('geo_regions'), lazy='dynamic')
    hist_places         = db.relationship('HistPlace', secondary=geo_regions_hist_places, backref=db.backref('geo_regions'), lazy='dynamic')
    processes           = db.relationship('Process', secondary=geo_regions_processes, backref=db.backref('geo_regions'), lazy='dynamic')
    facts               = db.relationship('Fact', secondary=geo_regions_facts, backref=db.backref('geo_regions'), lazy='dynamic')
    subregions          = db.relationship('GeoRegion',
                                        secondary=geo_regions_sub_geo_regions,
                                        primaryjoin=id==geo_regions_sub_geo_regions.c.parent_id,
                                        secondaryjoin=id==geo_regions_sub_geo_regions.c.child_id,
                                        backref="parent_regions")

    def __repr__(self):
        return '<Geographical region %r, shows as %r>' % (self.name, self.label)
