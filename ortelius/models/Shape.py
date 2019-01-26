from sqlalchemy.ext.hybrid import hybrid_property
from geoalchemy2.types import Geometry

from ortelius.database import db


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
        self.shape_type = shape_type
        self.start_date = start_date
        self.end_date = end_date
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.stroke_opacity = stroke_opacity
        self.fill_opacity = fill_opacity
        self.coordinates = coordinates

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.TIMESTAMP, nullable=True)
    end_date = db.Column(db.TIMESTAMP, nullable=True)
    shape_type = db.Column(db.Enum('Point', 'Polygon', 'Multipolygon', 'Multipoint', name='shape_types'))
    order_num = db.Column(db.Integer)
    point = db.Column(Geometry(geometry_type='POINT', srid=4326), default=None)
    multipoint = db.Column(Geometry(geometry_type='MULTIPOINT', srid=4326), default=None)
    polygon = db.Column(Geometry(geometry_type='POLYGON', srid=4326), default=None)
    multipolygon = db.Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), default=None)

    @hybrid_property
    def coordinates(self):
        if self.shape_type == 'Point':
            return self.point
        if self.shape_type == 'Polygon':
            return self.polygon
        if self.shape_type == 'Multipolygon':
            return self.multipolygon
        if self.shape_type == 'Multipoint':
            return self.multipoint
        return self.point

    @coordinates.setter
    def coordinates(self, coordinates):
        if self.shape_type == 'Point':
            self.point = coordinates
        if self.shape_type == 'Polygon':
            self.polygon = coordinates
        if self.shape_type == 'Multipolygon':
            self.multipolygon = coordinates
        if self.shape_type == 'Multipoint':
            self.multipoint = coordinates

    stroke_color = db.Column(db.String(255))
    fill_color = db.Column(db.String(255))
    stroke_opacity = db.Column(db.Float, default=1)
    fill_opacity = db.Column(db.Float, default=1)

    def __repr__(self):
        try:
            string = '<Shape, id: {0}>'.format(self.id)
        except Exception:
            string = '<Shape, id not assigned>'
        return string
