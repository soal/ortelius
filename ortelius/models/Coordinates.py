import bisect
import sqlalchemy
from sqlalchemy.ext.orderinglist import ordering_list
from geoalchemy2.types import Geometry

from ortelius.database import db
from ortelius.models.Date import Date


# class Coordinates(db.Model):
#     """Coordinates model"""
#     __tablename__ = 'coordinates'
#
#     def __init__(self, lat=None, long=None, quadrant=None, position=None):
#         self.lat = lat
#         self.long = long
#         self.quadrant = quadrant
#         self.position = position
#
#     id            = db.Column(db.Integer, primary_key=True)
#     lat           = db.Column(db.Float, nullable=False)
#     long          = db.Column(db.Float, nullable=False)
#     quadrant_hash = db.Column(db.String, db.ForeignKey('quadrant.hash'), nullable=True)
#     quadrant      = db.relationship('Quadrant', backref=db.backref('coordinates', uselist=True), uselist=False)
#     shape_id      = db.Column(db.Integer, db.ForeignKey('shape.id'), nullable=True)
#     position      = db.Column(db.Integer)
#
#     @classmethod
#     def create(cls, lat, long, quadrant=None):
#         """
#         Create or get coordinates if it's already exist.
#         Coordinates.create(lat=[lattitude:float|int], long=[longitude:float|int], [quadrant=[Quadrant]])
#         lat and long should be floats or ints, optional arg quadrant instance of Quadrant class
#         """
#         if not lat or not long:
#             raise sqlalchemy.exc.ArgumentError('Fields required: lat, long')
#
#         if not quadrant:
#             quadrant = Quadrant.get(lat, long)
#
#             if not quadrant:
#                 raise sqlalchemy.exc.ArgumentError('Can\'t find quadrant and none quadrant given')
#
#         return cls(lat=lat, long=long, quadrant=quadrant)
#
#     def __repr__(self):
#         return '<Coordinates point, id: %i, lat: %i, long: %i>' % (self.id, self.lat, self.long)



class Shape(db.Model):
    """Shape model"""
    __tablename__ = 'shape'

    def __init__(self,
                 start_date=None,
                 end_date=None,
                #  coordinates=[],
                 stroke_color=None,
                 stroke_opacity=None,
                 fill_color=None,
                 fill_opacity=None,
                 type='Polygon'):
        self.start_date = start_date
        self.end_date = end_date
        # self.coordinates = coordinates
        self.stroke_color = stroke_color
        self.fill_color = fill_color
        self.stroke_opacity = stroke_opacity
        self.fill_opacity = fill_opacity
        self.type = type

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
    # coordinates    = db.relationship('Coordinates',
    #                                  backref=db.backref('shape', uselist=False),
    #                                  order_by='Coordinates.position',
    #                                  collection_class=ordering_list('position'))
    coordinates    = db.Column(Geometry('MULTIPOLYGON'))
    type           = db.Column(db.Enum('Polygon', 'Dot', 'Route', 'Movement', name='shape_types'))  # NOTE: may be separate table?
    stroke_color   = db.Column(db.String(255))
    fill_color     = db.Column(db.String(255))
    stroke_opacity = db.Column(db.Float, default=1)
    fill_opacity   = db.Column(db.Float, default=1)

    # def __repr__(self):
    #     return '<Shape, id: {id}>'.format(self.id)



# class Quadrant(db.Model):
#     """Quadrant model"""
#     __tablename__ = 'quadrant'
#
#     def __init__(self, hash=None):
#         self.hash = hash
#
#     hash = db.Column(db.String(9), primary_key=True, autoincrement=False)
#     # coordinates is declared in Coordinates class via backref
#
#     quadrants = [(x, y) for y in range(-180, 180, 4) for x in range(-180, 180, 4)]
#
#     @classmethod
#     def calc(cls, lat, long):
#         lats = [q[0] for q in cls.quadrants]
#         longs = [q[1] for q in cls.quadrants]
#         lat_value = lats[bisect.bisect_left(lats, lat)]  # NOTE: check that bisect_left returns proper position
#         long_value = longs[bisect.bisect(longs, long) - 1]
#         return [lat_value, long_value]
#
#     @classmethod
#     def make_hash(cls, lat, long):
#         qs = cls.calc(lat, long)
#         return ','.join([str(qs[0]), str(qs[1])])
#
#     @classmethod
#     def get(cls, lat, long):
#         quadrant_id = cls.make_hash(lat, long)
#         return db.query(cls).get(quadrant_id)
