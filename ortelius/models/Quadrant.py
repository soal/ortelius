from ortelius import db
import bisect


class Quadrant(db.Model):
    """Quadrant model"""
    __tablename__ = 'quadrant'

    def __init__(self, hash=None):
        self.hash = hash

    hash = db.Column(db.String(9), primary_key=True, autoincrement=False)
    # facts is declared in Fact model via backref

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
        lat_value = lats[bisect.bisect_left(lats, lat)]  # TODO: check that bisect_left returns proper position
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
