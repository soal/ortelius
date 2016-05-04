def serialize(sqlalchemy_obj):
    serialized = {}
    for field in sqlalchemy_obj._sa_class_manager.mapper.mapped_table.columns.keys():
        serialized[field] = sqlalchemy_obj.__getattribute__(field)
    return serialized

def convert_wikitext(wikitext):
    from smc import mw
    from lxml import etree

    ast = mw.MediaWiki(wikitext).ast
    div = etree.Element('div')
    elements = ast.getchildren()[0].getchildren()[0]
    for elem in elements:
        div.append(elem)

    return etree.tounicode(div)
