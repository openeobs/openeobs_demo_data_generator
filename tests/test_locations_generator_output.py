import unittest
from datetime import datetime
from demo_data_generators.locations import LocationsGenerator


class TestLocationsGeneratorOutput(unittest.TestCase):
    """
    Test that the locations generator does indeed generate locations
    """

    def setUp(self):
        """
        Setup an example generator instance so can use the record
        """
        gen = LocationsGenerator('a', 1)
        records = gen.data.findall('record')
        self.ward_record = records[0]
        self.bed_record = records[1]

    def test_ward_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.ward_record.attrib['id'],
                         'nhc_def_conf_location_wa',
                         'Incorrect ID ')
        self.assertEqual(self.ward_record.attrib['model'],
                         'nh.clinical.location',
                         'Incorrect model')

    def test_bed_record(self):
        """
        Make sure the record has teh correct id and model
        """
        self.assertEqual(self.bed_record.attrib['id'],
                         'nhc_def_conf_location_wa_b1',
                         'Incorrect ID ')
        self.assertEqual(self.bed_record.attrib['model'],
                         'nh.clinical.location',
                         'Incorrect model')

    def test_ward_name(self):
        """
        Make sure that the name field is correct
        """
        field = self.ward_record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'Ward A', 'Name field incorrect')

    def test_bed_name(self):
        """
        Make sure that the name field is correct
        """
        field = self.bed_record.find('field[@name=\'name\']')
        self.assertEqual(field.text, 'Bed 1',  'Name field incorrect')

    def test_ward_code(self):
        """
        Make sure that the code field is correct
        """
        field = self.ward_record.find('field[@name=\'code\']')
        self.assertEqual(field.text, 'A', 'Code field incorrect')

    def test_bed_code(self):
        """
        Make sure that the code field is correct
        """
        field = self.bed_record.find('field[@name=\'code\']')
        self.assertEqual(field.text, 'A1', 'Code field incorrect')

    def test_ward_type(self):
        """
        Make sure that the type field is correct
        """
        field = self.ward_record.find('field[@name=\'type\']')
        self.assertEqual(field.text, 'poc', 'Type field incorrect')

    def test_bed_type(self):
        """
        Make sure that the type field is correct
        """
        field = self.bed_record.find('field[@name=\'type\']')
        self.assertEqual(field.text, 'poc', 'Type field incorrect')

    def test_ward_usage(self):
        """
        Make sure that the usage field is correct
        """
        field = self.ward_record.find('field[@name=\'usage\']')
        self.assertEqual(field.text, 'ward', 'Usage field incorrect')

    def test_bed_usage(self):
        """
        Make sure that the usage field is correct
        """
        field = self.bed_record.find('field[@name=\'usage\']')
        self.assertEqual(field.text, 'bed', 'Usage field incorrect')

    def test_ward_parent_id(self):
        """
        Make sure the parent id is correct
        """
        field = self.ward_record.find('field[@name=\'parent_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_def_conf_location_guh',
                         'Incorrect parent id defined')

    def test_bed_parent_id(self):
        """
        Make sure the parent id is correct
        """
        field = self.bed_record.find('field[@name=\'parent_id\']')
        self.assertEqual(field.attrib['ref'], 'nhc_def_conf_location_wa',
                         'Incorrect parent id defined')