from xml.etree.ElementTree import Element, SubElement


class Field(object):

    def __init__(self, record, attributes):
        self._create(self, record, attributes)

    def _create(self, record, attributes):
        self.element = SubElement(record, 'field', attributes)


class Record(object):

    def __init__(self, data, attributes):
        self._create(self, data, attributes)

    def _create(self, data, attributes):
        self.element = SubElement(data, 'record', attributes)

    def append(self, attributes):
        Field(self.element, attributes)


class XMLBuilder(object):

    def __init__(self):
        self.document = Element('openerp')
        self.data = SubElement(self.document, 'data', {'noupdate': '1'})

    def record(self, attributes):
        return Record(self.data, attributes)

