from sqlalchemy.dialects.postgresql import JSONB

from ortelius.database import db
from ortelius.models.Shape import Shape
from ortelius.types.historical_date import HDate


elements_subelements = db.Table('elements_subelements',
    db.Column('parent_id', db.Integer, db.ForeignKey('element.id')),
    db.Column('child_id', db.Integer, db.ForeignKey('element.id'))
)

Shape.element_id = db.Column(db.Integer, db.ForeignKey('element.id'))


class Element(db.Model):
    """Element model"""
    __tablename__ = 'element'

    def __init__(self,
                 name=None,
                 label=None,
                 description=None,
                 start_date=None,
                 end_date=None,
                 shapes=None,
                 text=None,
                 element_type=None,
                 weight=None,
                 trusted=False
                ):
        self.name = name
        self.label = label
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.shapes = shapes
        self.text = text
        self.element_type = element_type
        self.weight = weight
        self.trusted = trusted

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String(255), nullable=False, unique=True, index=True)
    label             = db.Column(db.Unicode(255))
    description       = db.Column(db.UnicodeText, server_default='No description')
    start_date        = db.Column(HDate, nullable=True)
    end_date          = db.Column(HDate, nullable=True)
    shapes            = db.relationship('Shape', backref=db.backref('element', uselist=False))
    text              = db.Column(db.UnicodeText, server_default='No text')
    type_name         = db.Column(db.String, db.ForeignKey('element_type.name'), nullable=True, index=True)
    subelements       = db.relationship('Element',
                                        secondary=elements_subelements,
                                        primaryjoin=id == elements_subelements.c.parent_id,
                                        secondaryjoin=id == elements_subelements.c.child_id,
                                        backref="parent_processes")
    # subelements       = db.relationship('Element', secondary=elements_subelements)
    trusted           = db.Column(db.Boolean)
    weight            = db.Column(db.Integer, nullable=False, server_default='1')

    def __repr__(self):
        return '<Element %r, shows as %r>' % (self.name, self.label)


class ElementType(db.Model):
    """ElementType model"""
    __tablename__ = 'element_type'

    def __init__(self, name=None, label=None, elements=None):
        self.name = name
        self.label = label
        self.elements = elements

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), index=True, unique=True)
    label       = db.Column(db.Unicode(120), nullable=False, unique=True)
    elements    = db.relationship('Element', backref=db.backref('element_type', uselist=False), lazy='dynamic')
    work_schema = db.Column(JSONB, nullable=True)

    def __repr__(self):
        return '<Element type %r, shows as %r>' % (self.name, self.label)
