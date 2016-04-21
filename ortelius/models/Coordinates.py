import bisect
import sqlalchemy

from ortelius import db
from ortelius.models.Date import Date


shapes_coordinates = db.Table('shapes_coordinates',
    db.Column('shape_id', db.Integer, db.ForeignKey('shape.id')),
    db.Column('coordinates_id', db.Integer, db.ForeignKey('coordinates.id'))
)


class Coordinates(db.Model):
    """Coordinates model"""
    __tablename__ = 'coordinates'

    def __init__(self, lat=None, long=None, quadrant=None):
        self.lat = lat
        self.long = long
        self.quadrant = quadrant

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    quadrant_hash = db.Column(db.String, db.ForeignKey('quadrant.hash'), nullable=True)
    quadrant = db.relationship('Quadrant', backref=db.backref('coordinates', uselist=True), uselist=False)
    # shapes is declared in Shape class via backref

    @classmethod
    def create(cls, lat=None, long=None, quadrant=None):
        """
            Create or get coordinates if it's already exist.
            Coordinates.create(lat=[lattitude:float|int], long=[longitude:float|int], [quadrant=[Quadrant]])
            lat and long should be floats or ints, optional arg quadrant instance of Quadrant class
        """
        if not lat or not long:
            raise sqlalchemy.exc.ArgumentError('Fields required: lat, long')

        if not quadrant:
            quadrant = Quadrant.get(lat, long)

        point = cls.query.filter(Coordinates.lat == lat, Coordinates.long == long).first()

        if point:
            return point

        return cls(lat=lat, long=long, quadrant=quadrant)



class Shape(db.Model):
    """Shape model"""
    __tablename__ = 'shape'

    def __init__(self, start_date=None, end_date=None, coordinates=None):
        self.start_date = start_date
        self.end_date = end_date
        self.coordinates = coordinates

    id = db.Column(db.Integer, primary_key=True)
    start_date_id = db.Column(db.Integer, db.ForeignKey('date.id'))
    end_date_id = db.Column(db.Integer, db.ForeignKey('date.id'))
    start_date = db.relationship('Date', backref=db.backref('shapes_started', uselist=True, lazy='dynamic'), uselist=False, foreign_keys=start_date_id)
    end_date = db.relationship('Date', backref=db.backref('shapes_ended', uselist=True, lazy='dynamic'), uselist=False, foreign_keys=end_date_id)
    coordinates = db.relationship('Coordinates',
                                  secondary=shapes_coordinates,
                                  backref=db.backref('shapes', lazy='dynamic'))

    def __repr__(self):
        return '<Shape, id: %i>' % (self.id)



class Quadrant(db.Model):
    """Quadrant model"""
    __tablename__ = 'quadrant'

    def __init__(self, hash=None):
        self.hash = hash

    hash = db.Column(db.String(9), primary_key=True, autoincrement=False)
    # coordinates is declared in Coordinates class via backref

    @classmethod
    def make_list(cls):
        qts = []
        for x in range(-180, 180, 4):
            for y in range(-180, 180, 4):
                qts.append([x, y])

        cls.quadrants = qts

    quadrants = []

    @classmethod
    def calc(cls, lat, long):
        lats = [q[0] for q in cls.quadrants]
        longs = [q[1] for q in cls.quadrants]
        lat_value = lats[bisect.bisect_left(lats, lat)]  # NOTE: check that bisect_left returns proper position
        long_value = longs[bisect.bisect(longs, long) - 1]
        return [lat_value, long_value]

    @classmethod
    def make_hash(cls, lat, long):
        qs = cls.calc(lat, long)
        return ','.join([str(qs[0]), str(qs[1])])

    @classmethod
    def get(cls, lat, long):
        quadrant_id = cls.make_hash(lat, long)
        return cls.query.get(quadrant_id)



