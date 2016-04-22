def serialize(sqlalchemy_obj):
    serialized = {}
    for field in sqlalchemy_obj._sa_class_manager.mapper.mapped_table.columns.keys():
        serialized[field] = sqlalchemy_obj.__getattribute__(field)
    return serialized
