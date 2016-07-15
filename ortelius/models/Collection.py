from ortelius.database import db
from ortelius.models.Element import Element

collection_links = db.Table('hm_collection_links',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('hm_collections.id')),
    db.Column('element_id', db.Integer, db.ForeignKey('hm_elements.id'))
)


ordered_collection_liks = db.Table('hm_ordcollection_links',
    db.Column('id', db.Integer),
    db.Column('ordcollection_id', db.Integer, db.ForeignKey('hm_ordcollections.id')),
    db.Column('element_id', db.Integer, db.ForeignKey('hm_elements.id')),
    db.Column('order_num', db.Integer, nullable=False),
    db.Column('start_date', db.TIMESTAMP),
    db.Column('start_date_id', db.Integer),
    db.Column('end_date', db.TIMESTAMP),
    db.Column('end_date_id', db.Integer)
)


ordered_collection_order = db.Table('hm_ordcollection_order',
    db.Column('id', db.Integer),
    db.Column('ordcollection_id', db.Integer, db.ForeignKey('hm_ordcollections.id')),
    db.Column('a_element_id', db.Integer, db.ForeignKey('hm_elements.id')),
    db.Column('b_element_id', db.Integer, db.ForeignKey('hm_elements.id')),
    db.Column('a_end_date', db.TIMESTAMP),
    db.Column('a_end_date_id', db.Integer),
    db.Column('b_start_date', db.TIMESTAMP),
    db.Column('b_start_date_id', db.Integer)
)


class Collection(db.Model):
    """Collection model"""
    __tablename__ = 'hm_collections'

    def __init__(self, name=None, label=None, elements=None):
        self.name = name
        self.label = label
        self.elements = elements

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False, unique=True, index=True)
    label       = db.Column(db.Unicode(255), index=True)

    elements    = db.relationship('Element', secondary=collection_links, backref=db.backref('collections', lazy='dynamic'))


class OrderedCollection(db.model):
    """OrderedCollection model"""
    __tablename__ = 'hm_ordcollections'

    def __init__(self, name=None, label=None, elements=None, ordered_collections=None):
        self.name = name
        self.label = label
        self.elements = elements
        self.ordered_collections = ordered_collections

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False, unique=True, index=True)
    label       = db.Column(db.Unicode(255), index=True)

    elements = db.relationship('Element', secondary=ordered_collection_liks, backref=db.backref('ordered_collections', lazy='dynamic'))
