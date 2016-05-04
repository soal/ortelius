def serialize(sqlalchemy_obj):
    serialized = {}
    for field in sqlalchemy_obj._sa_class_manager.mapper.mapped_table.columns.keys():
        serialized[field] = sqlalchemy_obj.__getattribute__(field)
    return serialized

def convert_wikitext(wikitext):
    from smc import mw
    from lxml import etree, html
    from lxml.html import clean

    ast = mw.MediaWiki(wikitext).as_string()
    cleaner = clean.Cleaner(remove_tags=['html', 'body', 'pre'], remove_unknown_tags=False)
    cleaned = cleaner.clean_html(html.fromstring(ast))

    return etree.tounicode(cleaned)
