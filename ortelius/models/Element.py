import datetime
import enum
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql import JSON

from ortelius.database import db
from ortelius.models.Shape import Shape
from ortelius.models.User import User

# from ortelius.types.historical_date import HDate

# class ConnectionTypes(ENUM):
#     ParentChild = 'ParentChild'
#     Horisontal  = 'Horisontal'


element_links = db.Table('hm_element_links',
    db.Column('parent_element_id', db.Integer, db.ForeignKey('hm_elements.id')),
    db.Column('child_element_id', db.Integer, db.ForeignKey('hm_elements.id')),
    db.Column('connection_type', ENUM('ParentChild', 'Horisontal', name='connection_types'), nullable=False),
    db.Column('weight', db.Integer, nullable=False),
    db.Column('link_start_date', db.TIMESTAMP),
    db.Column('link_start_date_id', db.Integer),
    db.Column('link_end_date', db.TIMESTAMP),
    db.Column('link_end_date_id', db.Integer)
)

Shape.element_id = db.Column(db.Integer, db.ForeignKey('hm_elements.id'))


class Element(db.Model):
    """Element model"""
    __tablename__ = 'hm_elements'

    def __init__(self,
                 name,
                 label,
                 description=None,
                 start_date=None,
                 end_date=None,
                 shapes=None,
                 text=None,
                 element_type=None,
                 weight=None,
                 trusted=0
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
    description       = db.Column(db.UnicodeText, server_default="No description")
    # info              = db.Column(JSON, server_default="")
    weight            = db.Column(db.Integer, nullable=False, server_default='5', index=True)
    start_date        = db.Column(db.TIMESTAMP, nullable=True)
    start_date_id     = db.Column(db.Integer, nullable=True)
    end_date          = db.Column(db.TIMESTAMP, nullable=True)
    end_date_id       = db.Column(db.Integer, nullable=True)
    element_type_id   = db.Column(db.Integer, db.ForeignKey('hm_element_types.id'), nullable=True, index=True)
    text              = db.Column(db.UnicodeText, server_default='No text')
    trusted           = db.Column(db.Numeric, server_default='0')
    edit_date         = db.Column(db.TIMESTAMP)
    user_id           = db.Column(db.Integer, db.ForeignKey('hm_users.id'), nullable=True)

    children          = db.relationship('Element',
                                        secondary=element_links,
                                        primaryjoin=id == element_links.c.parent_element_id,
                                        secondaryjoin=db.and_(id == element_links.c.child_element_id,
                                                              element_links.c.connection_type == 'ParentChild'),
                                        backref="parent_elements")
    # subelements       = db.relationship('Element', secondary=elements_subelements)
    # shapes              = db.relationship('Shape', backref=db.backref('element', uselist=False))
    # ordered_collections = db.relationship('OrderedCollection')

    def __repr__(self):
        return '<Element %r, shows as %r>' % (self.name, self.label)

class ValueTypes(enum.Enum):
    date_value   = 'date_value'
    int_value    = 'int_value'
    float_value  = 'float_value'
    string_value = 'string_value'

element_type_info_fields = db.Table('hm_element_type_info_fields',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('element_type_id', db.Integer, db.ForeignKey('hm_element_types.id')),
    db.Column('field_order', db.Integer),
    db.Column('field_name', db.String(255), nullable=False),
    #db.Column('field_type', ENUM(ValueTypes, name='wtf'), nullable=False),
    # db.Column('field_type', ENUM(ValueTypes, name='value_types'), nullable=False),
    db.Column('description', db.String(255), server_default=""),
    db.Column('weight', db.Integer, default=5, nullable=False)
)

class ElementInfo(db.Model):
    """ElementInfo model"""
    __tablename__ = 'hm_element_info'

    def __init__(self):
        pass

    id                = db.Column(db.Integer, primary_key=True)
    element_id        = db.Column(db.Integer, db.ForeignKey('hm_elements.id'), nullable=False)
    field_id          = db.Column(db.Integer, db.ForeignKey('hm_element_type_info_fields.id'), nullable=False)

    date_value        = db.Column(db.TIMESTAMP)
    int_value         = db.Column(db.Integer)
    float_value       = db.Column(db.Float)
    string_value      = db.Column(db.String(255))

    #     target_element_id integer, -- избыточное, для потенциальной пересылки

    start_date        = db.Column(db.TIMESTAMP, nullable=True)
    start_date_id     = db.Column(db.Integer, nullable=True)
    end_date          = db.Column(db.TIMESTAMP, nullable=True)
    end_date_id       = db.Column(db.Integer, nullable=True)

# trusted decimal DEFAULT 1,
    edit_date         = db.Column(db.TIMESTAMP)
    user_id           = db.Column(db.Integer, db.ForeignKey('hm_users.id'), nullable=True)

class ElementType(db.Model):
    """ElementType model"""
    __tablename__ = 'hm_element_types'

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
