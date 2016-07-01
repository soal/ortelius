from geoalchemy2.types import Geometry

from ortelius.database import db
from ortelius.types.historical_date import HDate

class Shape(db.Model):
    """Shape model"""
    __tablename__ = 'shape'

    def __init__(self,
                 start_date=None,
                 end_date=None,
                 coordinates=None,
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
    start_date     = db.Column(HDate, nullable=True)
    end_date       = db.Column(HDate, nullable=True)
    point          = db.Column(Geometry(geometry_type='POINT', srid=4326), default=None)
    multipoint     = db.Column(Geometry(geometry_type='MULTIPOINT', srid=4326), default=None)
    polygon        = db.Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), default=None)
    shape_type     = db.Column(db.Enum('Area', 'Point', 'Route', 'Movement', name='shape_types'))  # NOTE: may be separate table?
    stroke_color   = db.Column(db.String(255))
    fill_color     = db.Column(db.String(255))
    stroke_opacity = db.Column(db.Float, default=1)
    fill_opacity   = db.Column(db.Float, default=1)

    def __repr__(self):
        return '<Shape, id: {1}>'.format(self.id if self.id else 'not assigned')
