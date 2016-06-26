# import bisect
# import sqlalchemy
# from sqlalchemy.ext.orderinglist import ordering_list
from geoalchemy2.types import Geometry

from ortelius.database import db
from ortelius.models.Date import Date


class Shape(db.Model):
    """Shape model"""
    __tablename__ = 'shape'

    def __init__(self,
                 start_date=None,
                 end_date=None,
                 coordinates=[],
                 stroke_color=None,
                 stroke_opacity=None,
                 fill_color=None,
                 fill_opacity=None,
                 shape_type='Point'):
        self.start_date = start_date
        self.end_date = end_date
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.stroke_opacity = stroke_opacity
        self.fill_opacity = fill_opacity
        self.shape_type = shape_type
        if shape_type == 'Point':
            self.point = coordinates
        if shape_type == 'Route':
            self.multipoint = coordinates
        if shape_type == 'Movement':
            self.multipoint = coordinates
        if shape_type == 'Area':
            self.polygon = coordinates  # Area ALWAIS stores as multipolygon


    id             = db.Column(db.Integer, primary_key=True)
    start_date_id  = db.Column(db.Integer, db.ForeignKey('date.id'))
    end_date_id    = db.Column(db.Integer, db.ForeignKey('date.id'))
    start_date     = db.relationship('Date',
                                     backref=db.backref('shapes_started', uselist=True, lazy='dynamic'),
                                     uselist=False,
                                     foreign_keys=start_date_id)
    end_date       = db.relationship('Date',
                                     backref=db.backref('shapes_ended', uselist=True, lazy='dynamic'),
                                     uselist=False,
                                     foreign_keys=end_date_id)
    point          = db.Column(Geometry(geometry_type='POINT', srid=4326), default=None)
    multipoint     = db.Column(Geometry(geometry_type='MULTIPOINT', srid=4326), default=None)
    polygon        = db.Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), default=None)
    shape_type           = db.Column(db.Enum('Polygon', 'Point', 'Route', 'Movement', name='shape_types'))  # NOTE: may be separate table?
    stroke_color   = db.Column(db.String(255))
    fill_color     = db.Column(db.String(255))
    stroke_opacity = db.Column(db.Float, default=1)
    fill_opacity   = db.Column(db.Float, default=1)

    def __repr__(self):
        return '<Shape, id: {id}>'.format(self.id)
