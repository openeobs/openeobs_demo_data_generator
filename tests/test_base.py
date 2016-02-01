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