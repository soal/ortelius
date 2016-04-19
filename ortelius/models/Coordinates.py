import bisect
from ortelius import db
from ortelius.models.Date import Date


shapes_coordinates = db.Table('shapes_coordinates',
    db.Column('shape_id', db.Integer, db.ForeignKey('shape.id')),
    db.Column('coordinates_id', db.Integer, db.ForeignKey('coordinates.id'))
)


class Coordinates(db.Model):
    """Coordinates model"""
    __tablename__ = 'coordinates'

    def __init__(self, lat=None, long=None):
        self.lat = lat
        self.long = long

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    # quadrant is declared in Quadrant class via backref
    # shapes is declared in Shape class via backref


class Quadrant(db.Model):
    """Quadrant model"""
    __tablename__ = 'quadrant'

    def __init__(self, hash=None, coordinates=None):
        self.hash = hash
        self.coordinates = coordinates

    hash = db.Column(db.String(9), primary_key=True, autoincrement=False)
    coordinates = db.relationship('Coordinates', backref=db.backref('quadrant', uselist=False), lazy='joined')

    @classmethod
    def make_quadrants(cls):
        qts = []
        for x in range(-180, 180, 4):
            for y in range(-180, 180, 4):
                qts.append([x, y])

        cls.quadrants = qts

    quadrants = []

    @classmethod
    def calc_quadrant(cls, lat, long):
        lats = [q[0] for q in cls.quadrants]
        longs = [q[1] for q in cls.quadrants]
        lat_value = lats[bisect.bisect_left(lats, lat)]  # TODO: check that bisect_left returns prope position
        long_value = longs[bisect.bisect(longs, long) - 1]
        return [lat_value, long_value]

    @classmethod
    def hash_quadrant(cls, lat, long):
        qs = cls.calc_quadrant(lat, long)
        return ','.join([str(qs[0]), str(qs[1])])

    @classmethod
    def get_quadrant(cls, lat, long):
        quadrant_id = cls.hash_quadrant(lat, long)
        return cls.query.get(quadrant_id)


class Shape(db.Model):
    """Shape model"""
    __tablename__ = 'shape'

    def __init__(self, start_date=None, end_date=None, coordinates=None):
        self.start_date = start_date
        self.end_date = end_date
        self.coordinates = coordinates

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Integer, db.ForeignKey('date.id'))
    end_date = db.Column(db.Integer, db.ForeignKey('date.id'))
    coordinates = db.relationship('Coordinates',
                                  secondary=shapes_coordinates,
                                  backref=db.backref('shapes', lazy='dynamic'))
    # fact is declared in Fact class via backref
    # hist_region_id = db.Column(db.Integer, db.ForeignKey('hist_region.id'))
    # process = db.Column(db.Integer, db.ForeignKey('process.id'))
