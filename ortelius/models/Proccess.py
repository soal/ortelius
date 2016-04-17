# from ortelius import db
#
# processes_facts = db.Table('processes_facts',
#     db.Column('process_id', db.Integer, db.ForeignKey('process.id'))
#     db.Column('fact_id', db.Integer, db.ForeignKey('fact.id'))
# )
#
# processes_hist_regions = db.Table('processes_hist_regions',
#     db.Column('process_id', db.Integer, db.ForeignKey('process.id'))
#     db.Column('hist_region_id', db.Integer, db.ForeignKey('hist_region.id'))
# )
#
# processes_shapes = db.Table('processes_shapes',
#     db.Column('process_id', db.Integer, db.ForeignKey('process.id'))
#     db.Column('shape_id', db.Integer, db.ForeignKey('shape.id'))
# )
#
#
# class Process(db.Model):
#     """Process model"""
#     __tablename__ = 'process'
#
#     def __init__(self, arg):
#         super(Process, self).__init__()
#         self.arg = arg
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False, unique=True)
#     label = db.Column(db.Unicode(255), nullable=False)
#     description = db.Column(db.UnicodeText, server_default='No description')
#     weight = db.Column(db.Integer, nullable=False, server_default=5)  # NOTE: May be enum type?
#     process_type = db.Column(db.Integer, db.ForeignKey('process_type.id'))
#     start_date_millenium = db.Column(db.Integer, db.ForeignKey('millenium.name'), nullable=False)  # FIXME: What should be here???
#     start_date_century = db.Column(db.Integer, db.ForeignKey('century.name'), nullable=False)  # FIXME: What should be here???
#     start_date_year = db.Column(db.Date, db.ForeignKey('year.date'), nullable=False)  # FIXME: What should be here???
#     end_date_millenium = db.Column(db.Integer, db.ForeignKey('millenium.name'), nullable=True)  # FIXME: What should be here???
#     end_date_century = db.Column(db.Integer, db.ForeignKey('century.name'), nullable=True)  # FIXME: What should be here???
#     end_date_year = db.Column(db.Date, db.ForeignKey('year.date'), nullable=True)  # FIXME: What should be here???
#     text = db.Column(db.UnicodeText, server_default='No text')
#     hist_region = db.relationship('HistoricalRegion',
#                                   secondary=processes_hist_regions,
#                                   backref=db.backref('processes', lazy='dynamic'),
#                                   lazy='dynamic'
#                                   )
#     facts = db.relationship('Fact', secondary=processes_facts, backref=db.backref('processes', lazy='dynamic'), lazy='dynamic')
#     shapes = db.relationship('Shape', secondary=processes_shapes, lazy="joined")
#
#
# class ProcessType(db.Model):
#     """Process type model"""
#     __tablename__ = 'process_type'

    # def __init__(self, arg):
    #     super(ProcessType, self).__init__()
    #     self.arg = arg
