from xml.etree.ElementTree import Element, SubElement


class Field(object):

    def __init__(self, record, attributes):
        self._create(record, attributes)

    def _create(self, record, attributes):
        if 'value' in attributes:
            value = str(attributes['value'])
            del attributes['value']
        else:
            value = None

        self._element = SubElement(record, 'field', attributes)
        self.value = value

    @property
    def value(self):
        return self._element.text

    @value.setter
    def value(self, value):
        self._element.text = value

    @property
    def name(self):
        return self._element.attrib['name']

    @name.setter
    def name(self, value):
        self._element.attrib['name'] = value

    @property
    def ref(self):
        return self._element.attrib['ref']

    @ref.setter
    def ref(self, value):
        self._element.attrib['ref'] = value

    @property
    def eval(self):
        return self._element.attrib['eval']

    @eval.setter
    def eval(self, value):
        self._element.attrib['eval'] = value


class Record(object):

    def __init__(self, data, attributes):
        self._create(data, attributes)

    def _create(self, data, attributes):
        self._element = SubElement(data, 'record', attributes)

    def field(self, attributes):
        return Field(self._element, attributes)

    @property
    def model(self):
        return self._element.attrib['model']

    @model.setter
    def model(self, value):
        self._element.attrib['model'] = value

    @property
    def id(self):
        return self._element.attrib['id']

    @id.setter
    def id(self, value):
        self._element.attrib['id'] = value

    @property
    def context(self):
        return self._element.attrib['context']

    @context.setter
    def context(self, value):
        self._element.attrib['context'] = value


class Document(object):

    def __init__(self):
        self.document = Element('openerp')
        self.data = SubElement(self.document, 'data', {'noupdate': '1'})

    def record(self, attributes):
        return Record(self.data, attributes)
