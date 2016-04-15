from ortelius import db


class Fact(db.Model):
    """Fact model"""
    __tablename__ = 'facts_table'

    # def __init__(self, arg):
    #     super(Fact, self).__init__()
    #     self.arg = arg

    # id = db.Column(db.Integer, primary_key=True)

    # name = db.Column(db.String(255), nullable=False, unique=True)
    # label = db.Column(db.Unicode(255), nullable=False)
    # description = db.Column(db.UnicodeText, nullable=True, server_default='')
    # text = db.Column(db.UnicodeText, nullable=True, server_default='')
    # weight = db.Column(db.Integer, nullable=True, server_default=5)

    # start_date = db.relationship()
    # end_date = db.relationship()

    # shape = db.relationship('Shape',
    #                         secondary="facts_shape",
    #                         backref=db.backref('facts', lazy='dynamic'))
    # processes = db.relationship('Process',
    #                             secondary="facts_processes",
    #                             backref=db.backref('facts', lazy='dynamic'))

    # personas = db.relationship()
