from ortelius import db
from ortelius.models.Date import Date

shapes_coordinates = db.Table('shapes_coordinates',
    db.Column('shape_id', db.Integer, db.ForeignKey('shape.id')),
    db.Column('coordinates_id', db.Integer, db.ForeignKey('coordinates.id'))
)


class Shape(db.Model):
    """Shape model"""
    __tablename__ = 'shape'

    def __init__(self):
        pass

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Integer, db.ForeignKey('date.id'))
    end_date = db.Column(db.Integer, db.ForeignKey('date.id'))
    coordinates = db.relationship('Coordinates',
                                  secondary=shapes_coordinates,
                                  backref=db.backref('shapes', lazy='dynamic'))


class Coordinates(db.Model):
    """Coordinates model"""
    __tablename__ = 'coordinates'

    def __init__(self):
        pass

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    # shapes is declared in Shape class via backref
