from ortelius import db
from ortelius.models.Date import Date

shapes_coordinates = db.Table('shapes_coordinates',
    db.Column('shape_id', db.Integer, db.ForeignKey('shape.id')),
    db.Column('coordinates_id', db.Integer, db.ForeignKey('coordinates.id'))
)
