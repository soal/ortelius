from ortelius import db
import sqlalchemy
from ortelius.models.Date import Date
from ortelius.models.Coordinates import Shape


class Fact(db.Model):
    """Fact model"""
    __tablename__ = 'fact'

    def __init__(self,
                 name=None,
                 label=None,
                 description=None,
                 info=None,
                 weight=None,
                 type=None,
                 start_date=None,
                 end_date=None,
                 text=None,
                 shape=None,
                 trusted=False):
        self.name = name
        self.label = label
        self.description = description
        self.info = info
        self.weight = weight
        self.type = type
        self.text = text
        self.shape = shape
        self.start_date = start_date
        self.end_date = end_date
        self.trusted = False

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    label = db.Column(db.Unicode(255))
    description = db.Column(db.UnicodeText, server_default='No description')
    info = db.Column(db.UnicodeText, server_default='No info')
    weight = db.Column(db.Integer, nullable=False, server_default='5')  # NOTE: May be enum type? May be separate table?
    # NOTE: We need to reorganize dates handling
    start_date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    start_date = db.relationship('Date', backref=db.backref('facts_starts', lazy='dynamic'), foreign_keys=start_date_id)
    end_date_id = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)
    end_date = db.relationship('Date', backref=db.backref('facts_ends', lazy='dynamic'), foreign_keys=start_date_id)
    shape_id = db.Column(db.Integer, db.ForeignKey('shape.id'), nullable=True)
    shape = db.relationship('Shape', backref=db.backref('fact', uselist=False), uselist=False)
    type_name = db.Column(db.String, db.ForeignKey('fact_type.name'), nullable=True)
    text = db.Column(db.UnicodeText, server_default='No text')
    trusted = db.Column(db.Boolean)
    # hist_regions is declared in HistRegion model via backref
    # hist_places is declared in HistPlace model via backref
    # processes is declared in Process model via backref
    # personas is declared in Persona model via backref
    # georegions is declared in Georegion model via backref


    def __repr__(self):
        return '<Fact %s, shows as %s>' % (self.name, self.label)


class FactType(db.Model):
    """Fact types model"""
    __tablename__ = 'fact_type'

    def __init__(self, name=None, label=None):
        self.name = name
        self.label = label

    name = db.Column(db.String(120), primary_key=True)
    label = db.Column(db.Unicode(120), nullable=False, unique=True)
    facts = db.relationship('Fact', backref=db.backref('type', uselist=False), lazy='dynamic')

    @classmethod
    def create(cls, **kwargs):
        new_type = cls(**kwargs)
        db.session.add(new_type)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
        finally:
            return cls.query.get('name')

    def __repr__(self):
        return '<Fact type %r, shows as %r>' % (self.name, self.label)

