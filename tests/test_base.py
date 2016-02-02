from unittest import TestCase
from xml.etree.ElementTree import Element
from mock import patch

from demo_data_generators.base import Document, Record, Field


class TestField(TestCase):

    def setUp(self):
        self.record = Element('test_record')

    @patch('demo_data_generators.base.Field._create')
    def test_init_calls_create(self, mocked_create):
        mocked_create.return_value = None
        Field(self.record, {'name': 'test'})
        Field._create.assert_called_with(self.record, {'name': 'test'})

    def test_creating_Field_when_value_is_in_attributes(self):
        field = Field(self.record, {'value': 'test_value'})
        self.assertEqual(field.value, 'test_value')

    def test_creating_Field_when_no_value_is_in_attributes(self):
        field = Field(self.record, {})
        self.assertEqual(field.value, None)

    def test_creating_Field_when_value_is_not_str_coverts_to_str(self):
        field = Field(self.record, {'value': 1})
        self.assertEqual(field.value, '1')


class TestRecord(TestCase):

    def setUp(self):
        self.data = Element('test_data')

    @patch('demo_data_generators.base.Record._create')
    def test_init_calls_create(self, mocked_create):
        mocked_create.return_value = None
        Record(self.data, {'id': 'test_id'})
        Record._create.assert_called_with(self.data, {'id': 'test_id'})

    def test_field_returns_object_of_type_Field(self):
        record = Record(self.data, {})
        field = record.field({})
        self.assertEqual(type(field), Field)


class TestDocument(TestCase):

    def setUp(self):
        self.document = Document()

    def test_record_returns_object_of_type_Record(self):
        record = self.document.record({})
        self.assertEqual(type(record), Record)
