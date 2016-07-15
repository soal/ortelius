import datetime
from sqlalchemy.dialects.postgresql import JSON

from ortelius.database import db
from ortelius.models.Shape import Shape
from ortelius.models.User import User
# from ortelius.types.historical_date import HDate


element_links = db.Table('hm_element_links',
    db.Column('parent_element_id', db.Integer, db.ForeignKey('hm_elements.id')),
    db.Column('child_element_id', db.Integer, db.ForeignKey('hm_elements.id')),
    db.Column('weight', db.Integer),
    db.Column('link_start_date', db.TIMESTAMP),
    db.Column('link_start_date_id', db.Integer),
    db.Column('link_end_date_id', db.Integer)
)

Shape.element_id = db.Column(db.Integer, db.ForeignKey('hm_elements.id'))


class Element(db.Model):
    """Element model"""
    __tablename__ = 'hm_elements'

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
    label             = db.Column(db.Unicode(255), index=True)
    description       = db.Column(db.UnicodeText, server_default='No description')
    info              = db.Column(JSON, nullable=True)
    start_date        = db.Column(db.TIMESTAMP, nullable=True)
    start_date_id     = db.Column(db.Integer, nullable=True)
    end_date          = db.Column(db.TIMESTAMP, nullable=True)
    end_date_id       = db.Column(db.Integer, nullable=True)
    text              = db.Column(db.UnicodeText, server_default='No text')
    trusted           = db.Column(db.Numeric, server_default='0')
    edit_date         = db.Column(db.TIMESTAMP)
    weight            = db.Column(db.Integer, nullable=False, server_default='1', index=True)
    element_type_id   = db.Column(db.Integer, db.ForeignKey('hm_element_types.id'), nullable=True, index=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('hm_users.id'), nullable=True)

    children          = db.relationship('Element',
                                        secondary=element_links,
                                        primaryjoin=id == element_links.c.parent_element_id,
                                        secondaryjoin=id == element_links.c.child_element_id,
                                        backref="parent_elements")
    # subelements       = db.relationship('Element', secondary=elements_subelements)
    shapes              = db.relationship('Shape', backref=db.backref('element', uselist=False))
    ordered_collections = db.relationship('OrderedCollection')

    def __repr__(self):
        return '<Element %r, shows as %r>' % (self.name, self.label)


class ElementType(db.Model):
    """ElementType model"""
    __tablename__ = 'hm_elements_type'

    def __init__(self, name=None, label=None, elements=None):
        self.name = name
        self.label = label
        self.elements = elements

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), index=True, unique=True)
    label       = db.Column(db.Unicode(120), nullable=False, unique=True)
    elements    = db.relationship('Element', backref=db.backref('element_type', uselist=False), lazy='dynamic')
    schema      = db.Column(JSON, nullable=True)

    def __repr__(self):
        return '<Element type %r, shows as %r>' % (self.name, self.label)
