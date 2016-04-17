from ortelius import db
from ortelius.models.Date import Millenium, Century, Year, Date


class Fact(db.Model):
    """Fact model"""
    __tablename__ = 'fact'

    def __init__(self, name=None,
                 label=None,
                 description=None,
                 weight=None,
                 fact_type=None,
                 start_date=None,
                 end_date=None,
                 text=None,
                 shape=None):
        self.name = name
        self.label = label
        self.description = description
        self.weight = weight
        self.fact_type = fact_type
        self.text = text
        self.shape = shape
        if start_date:
            self.start_date = start_date[0]
            self.start_date_millenium = start_date[1]
            self.start_date_century = start_date[2]
            self.start_date_year = start_date[3]
        if end_date:
            self.end_date = end_date[0]
            self.end_date_millenium = end_date[1]
            self.end_date_century = end_date[2]
            self.end_date_year = end_date[3]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    label = db.Column(db.Unicode(255))
    description = db.Column(db.UnicodeText, server_default='No description')
    weight = db.Column(db.Integer, nullable=False, server_default='5')  # NOTE: May be enum type?
    fact_type = db.Column(db.Integer, db.ForeignKey('fact_type.id'))
    start_date_millenium = db.Column(db.Integer, db.ForeignKey('millenium.number'), nullable=True)  # FIXME: What should be here???
    start_date_century = db.Column(db.Integer, db.ForeignKey('century.number'), nullable=True)  # FIXME: What should be here???
    start_date_year = db.Column(db.Integer, db.ForeignKey('year.number'), nullable=True)  # FIXME: What should be here???
    start_date = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)  # FIXME: What should be here???
    end_date_millenium = db.Column(db.Integer, db.ForeignKey('millenium.number'), nullable=True)  # FIXME: What should be here???
    end_date_century = db.Column(db.Integer, db.ForeignKey('century.number'), nullable=True)  # FIXME: What should be here???
    end_date_year = db.Column(db.Integer, db.ForeignKey('year.number'), nullable=True)  # FIXME: What should be here???
    end_date = db.Column(db.Integer, db.ForeignKey('date.id'), nullable=True)  # FIXME: What should be here???
    text = db.Column(db.UnicodeText, server_default='No text')

    # shape = db.Column(db.Integer, db.ForeignKey('shape.id'))
    # shape = db.Column(db.Integer, db.ForeignKey('shape.id'))
    # processes is declared in Process model via backref
    # personas is declared in Persona model via backref
    # georegions is declared in Georegion model via backref
    # hist_regions is declared in Hist_region model via backref

    def __repr__(self):
        return '<Fact %s, shows as %s>' % (self.name, self.label)


class FactType(db.Model):
    """Fact types model"""
    __tablename__ = 'fact_type'

    def __init__(self, name=None, lable=None):
        self.name = name
        self.label = label

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    label = db.Column(db.Unicode(120), nullable=False, unique=True)
    type_facts = db.relationship('Fact', lazy='dynamic')

    def __repr__(self):
        return '<Fact type %r, shows as %r>' % (self.name, self.label)
