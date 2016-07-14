from ortelius.database import db
from ortelius.models.Element import Element


class Collection(db.Model):
    """Collection model"""
    __tablename__ = 'hm_collections'

    def __init__(self, name=None, label=None, elements=None, collections=None):
        self.name = name
        self.label = label
        self.elements = elements
        self.collections = collections

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(255), nullable=False, unique=True, index=True)
    label       = db.Column(db.Unicode(255), index=True)
    collections = db.relationship()
    elements    = db.relationship()



class OrderedCollection(db.model):
    """OrderedCollection model"""
    __tablename__ = 'hm_ordcollections'

    def __init__(self, name=None, label=None, elements=None, ordered_collections=None):
        self.name = name
        self.label = label
        self.elements = elements
        self.ordered_collections = ordered_collections
